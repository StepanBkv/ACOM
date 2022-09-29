require 'fox16'
require 'RMagick'
include Math
include Magick
include Fox

class Photo
  
  attr_reader :path
  
  def initialize(path)
    @path  = path
  end

end

class PhotoView < FXImageFrame

  def initialize(p, photo)
      super(p, nil)
      load_image(photo.path)
  end

  def load_image(path)
    File.open(path, "rb" ) do |io|
      self.image = FXJPGImage.new(app, io.read)
    end
  end

end

class AlbumView < FXMatrix  

  attr_reader :album

  def initialize(p, album)
    super(p, :opts => LAYOUT_FILL)
    @album = album
    @album.each { |photo| add_photo(photo) }
  end

  def add_photo(photo)
    PhotoView.new(self, photo)
  end


end

class ImageWindow < FXMainWindow

  def initialize(app)
    # Invoke base class initializer first
    super(app, 'Размытие Гаусса', opts: DECOR_ALL, width: 1420, height: 960)
     
   photo = ImageList.new("img/hb_2.jpg")
   # gauss_init(photo)
   oper_px = 2**8
   canny(photo, 3, 40*oper_px, 55*oper_px).write("img/canny_1_ruby.jpg")
   @album_view = AlbumView.new(self, [Photo.new("img/canny_1_ruby.jpg"), Photo.new("img/hb_2.jpg")])
    label1 = FXLabel.new(self, "С размытием.", :height => 40, :width => 160, :opts => LAYOUT_FIX_HEIGHT | LAYOUT_FIX_WIDTH|LAYOUT_FIX_X|LAYOUT_FIX_Y,
                           :x => 280, :y => 910)
    label2 = FXLabel.new(self, "Без размытия.", :height => 40, :width => 160, :opts => LAYOUT_FIX_HEIGHT | LAYOUT_FIX_WIDTH|LAYOUT_FIX_X|LAYOUT_FIX_Y,
                           :x => 1000, :y => 910)
    [label1, label2].each{|i| i.setFont(FXFont.new(app, "Times,125,bold")); i.backColor = 'blue'; i.textColor = "white"}
  end

  def create
    super
    # Make the main window appear
    show(PLACEMENT_SCREEN)
  end

  def gauss_init img
    n = 5
    matr_gauss = (0..n-1).map{|i|[]}
    sum_matr = 0 
    (0..n-1).each{|i| (0..n-1).each{|j| matr_gauss[i][j] = gauss(i,j); sum_matr += matr_gauss[i][j]}}
    (0..n-1).each{|i| (0..n-1).each{|j| matr_gauss[i][j] /= sum_matr}}
    gauss_blur = lambda {|ker, foto_grey|(0..697).each{|i| (0..883).each{|j| sum_value = (0..n-1).map{ |k| (0..n-1).map{ |l| ker[k][l]*foto_grey[0].pixel_color(i+k,j+l).red
      }.sum}.sum;foto_grey[0].pixel_color(i+2,j+2, Pixel.new(sum_value.to_i,sum_value.to_i,sum_value.to_i,65535))}}}
    gauss_blur.call matr_gauss, img
  end

  def gauss x, y
    a = b = 2
    sig = 2
    (1 / (2 * PI * sig ** 2)) * Math.exp(-((x - a) ** 2 + (y - b) ** 2) / (2 * sig ** 2))
  end

  def doubleFiltr lst_param
    begn = lst_param[1] / 2
    h, w = 700, 886
    end_h = h - begn
    end_w = w - begn
    for i in (begn..end_h)
        for j in (begn..end_w)
            if lst_param[0].pixel_color(i,j).red >= lst_param[3]
                lst_param[0].pixel_color(i,j, Pixel.new(65535,65535,65535,65535))
            elsif lst_param[0].pixel_color(i,j).red <= lst_param[2]
                lst_param[0].pixel_color(i,j, Pixel.new(0,0,0,65535))
            else
                cl_px = 65535 / 2
                lst_param[0].pixel_color(i,j, Pixel.new(cl_px,cl_px,cl_px,65535))
            end
    end
      end
    img = lst_param[0]
    img
  end

  def tang x, y
    if x != 0
        tg = y / x
    end

    if ((x>0 and y<0 and tg<-2.414) or (x<0 and y<0 and tg> 2.414))
       return 0
    elsif (x>0 and y<0 and tg<-0.414)
        return 1
    elsif ((x>0 and y<0 and tg>-0.414) or (x>0 and y>0 and tg< 0.414))
        return 2
    elsif (tg == -0.785)
        return 3
    elsif ((x>0 and y>0 and tg > 2.414) or (x<0 and y>0 and tg< -2.414))
        return 4
    elsif (x < 0 and y > 0 and tg < -0.414)
        return 5
    elsif ((x<0 and y>0 and tg>0.414) or (x<0 and y<0 and tg< 0.414))
        return 6
    elsif (x < 0 and y < 0 and tg < 2.414)
        return 7
    else
        return 0
    end

  end

  def sobel_operation img, size
    sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    begn = size / 2
    h, w = 700, 886
    end_h = h - begn 
    end_w = w - begn
    gv = img.copy
    gfi = (0..h-1).map{|i|[]}
    for i in (begn..end_h)
        for j in (begn..end_w)
            x = 0
            y = 0
            for k in (0..size-1)
                for l in (0..size-1)
                    x += sobel_x[k][l] * img[0].pixel_color((i - begn + k), (j - begn + l)).red
                    y += sobel_y[k][l] * img[0].pixel_color(i - begn + k, j - begn + l).red
            sqr = (Math.sqrt(x ** 2 + y ** 2)).to_i
            gv.pixel_color(i,j, Pixel.new(sqr.to_i, sqr.to_i, sqr.to_i, 65535))
            gfi[i][j] = tang(x, y)
    end
      end
        end
          end
    [gv, gfi]
  end

  def canny_alg img, size, low, high
    gvf_list = sobel_operation img, size

    h, w = 700, 886
    begn = size / 2 

    end_h = h - begn
    end_w = w - begn

    for i in (begn..end_h)
        for j in (begn..end_w)
            if  gvf_list[1][i][j] == 0 or gvf_list[1][i][j] == 4
                unless gvf_list[0].pixel_color(i, j+1).red < gvf_list[0].pixel_color(i, j).red and gvf_list[0].pixel_color(i, j).red > gvf_list[0].pixel_color(i, j-1).red
                    gvf_list[0].pixel_color(i, j, Pixel.new(0,0,0,65535))
              end
            end
            if gvf_list[1][i][j] == 1 or gvf_list[1][i][j] == 5
                unless gvf_list[0].pixel_color(i+1, j+1).red < gvf_list[0].pixel_color(i, j).red and gvf_list[0].pixel_color(i, j).red > gvf_list[0].pixel_color(i-1, j-1).red
                    gvf_list[0].pixel_color(i, j, Pixel.new(0,0,0,65535))
              end
            end
            if gvf_list[1][i][j] == 2 or gvf_list[1][i][j] == 6
                unless gvf_list[0].pixel_color(i+1, j).red < gvf_list[0].pixel_color(i, j).red and gvf_list[0].pixel_color(i, j).red > gvf_list[0].pixel_color(i-1, j).red
                    gvf_list[0].pixel_color(i, j, Pixel.new(0,0,0,65535))
              end
            end
            if gvf_list[1][i][j] == 3 or gvf_list[1][i][j] == 7
                unless gvf_list[0].pixel_color(i+1, j-1).red < gvf_list[0].pixel_color(i, j).red and gvf_list[0].pixel_color(i, j).red > gvf_list[0].pixel_color(i-1, j+1).red
                    gvf_list[0].pixel_color(i, j, Pixel.new(0,0,0,65535))
              end
            end
    end
      end          
    [gvf_list[0], size, low, high]
  end

  def canny img, size, low, high
    lst_param = canny_alg(img, size, low, high)
    doubleFiltr(lst_param)
  end
end

if __FILE__ == $0
    FXApp.new do |app|
        ImageWindow.new(app)
        app.create
        app.run
    end
end