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
     
   # photo = ImageList.new("img/hb_2.jpg")
   # gauss_init(photo)
   # photo.write("img/new_hb_2.jpg")
  @album_view = AlbumView.new(self, [Photo.new("img/new_hb_2.jpg"), Photo.new("img/hb_2.jpg")])
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
    gauss_blur matr_gauss, img 
  end

  def gauss x, y
    a = b = 2
    sig = 1
    (1 / (2 * PI * sig ** 2)) * Math.exp(-((x - a) ** 2 + (y - b) ** 2) / (2 * sig ** 2))
  end

  def gauss_blur ker, foto_grey
    for i in (0..697)
        for j in (0..883)
            sum_value = 0
            for k in (0..4)
                for l in (0..4)
                    sum_value += ker[k][l]*foto_grey[0].pixel_color(i+k,j+l).red
            foto_grey[0].pixel_color(i+2,j+2, Pixel.new(sum_value,sum_value,sum_value,65535))
    end
        end
            end
                end
    foto_grey
  end

end

if __FILE__ == $0
    FXApp.new do |app|
        ImageWindow.new(app)
        app.create
        app.run
    end
end