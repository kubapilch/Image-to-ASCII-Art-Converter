from PIL import Image
import sys, getopt

def load_image(file_name):
    return Image.open(file_name)

def create_image(width, height):
    return Image.new("RGB", (width, height))

def get_pixel(image:Image, row, column):
    width, height = image.size

    # Check if given cordinates are valid
    if row > width or column > height or column < 0 or row < 0:
        return None
    
    return image.getpixel((row, column))

def create_grayscale_image(image:Image, save=False):
    # Get the sie of an image
    width, height = image.size

    # New image in grayscale
    new = Image.new("RGB", (width, height))
    pixels = new.load()

    for i in range(width):
        for j in range(height):
            pixel = get_pixel(image, i, j)

            if pixel is None: continue
            
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]

            new_color = 0.299*red + 0.587*green + 0.114*blue

            pixels[i, j] = (int(new_color), int(new_color), int(new_color))
    
    if save:
        # Svae image to a file
        file_name = image.filename
        appending = file_name.split(".")[1]
        name = file_name.split(".")[0]

        new.save(f"{name}_Grayscale.{appending}")

        # Give new imge filename for ASCII converting
        new.filename = f"{name}_Grayscale.{appending}"

    return new

def get_average(image:Image):
    """
    Compute the avegare grey of all pixels in a tile
    """
    # Get the size of an image
    w, h = image.size

    # Create list of all pixels in a tile
    img_list = []
    for row in range(h):
        for col in range(w):
            img_list.append(get_pixel(image, col, row))
    
    # Return average grey of all pixels in a tile
    return sum([x[0] for x in img_list])/len(img_list)


def convert_to_ASCII_from_greyscale_from_imageObject(image:Image, output_file=None, cols=None, scale=0.43):
    # Get image size
    W, H = image.size

    # If columns not specified set as width of the image
    if cols is None:
        cols = W

    # Check if user-specified number of columns isn't too big for this image
    if cols > W:
        print("Too many columns for this image.")
        return

    # Dimensions of a tile
    w = int(W/cols)
    h = int(w/scale)

    # How many rows will image have
    rows = int(H/h)

    # Image variable
    image_in_ASCII = ""

    # Two sets of grey scale characters first one with 85 characters and the other one with 10
    # characters_scale1 = [chr(i) for i in range(38, 123)] # Scale = 3, 85 characters
    characters_scale2 = "qwertyuioa" # Scale = 25.5, 10 characters

    # Set spicified grey scale characters
    characters = characters_scale2
    scale = 255/len(characters)

    # Iterate through the image and create image in ASCII
    for row in range(rows):
        # Y conrdinates of a tile
        y1 = row*h
        y2 = (row+1)*h
        
        for col in range(cols):
            # X conrdinates of a tile
            x1 = col*w
            x2 = (col+1)*w

            # Cut tile
            im = image.crop((x1, y1, x2, y2))
            average_tone = get_average(im)

            # Check the average grey of a tile
            character = int(average_tone/scale)

            # To prevent index error
            if character == len(characters): character -= 1
            
            # Add character to the string with an image
            image_in_ASCII += characters[character]

        # Add new line
        image_in_ASCII += "\n"
    
    # Save image in ASCII to file
    if output_file is not None:
        if ".txt" not in output_file: output_file += ".txt"
    
        with open(output_file, "w") as f:
            f.write(image_in_ASCII)
    
    # Return image as a string if someone want to use it in a program
    return image_in_ASCII

def convert_to_ASCII_from_file(image_file_name, output_file=None, cols=None, scale=0.43):
    '''
    Accepts only file name that exist in script direcotry or specify full path to the file
    '''
    im = load_image(image_file_name)

    # Convert to greyscale image
    im = create_grayscale_image(im, False)

    # Convert to ASCII
    ascii_im = convert_to_ASCII_from_greyscale_from_imageObject(im, output_file, cols, scale)

    return ascii_im

def convert_to_ASCII_from_imageObject(image:Image, output_file=None, cols=None, scale=0.43):
    '''
    Accepts only Pillow Image Object
    '''
    # Convert to greyscale image
    im = create_grayscale_image(image, False)

    # Convert to ASCII
    ascii_im = convert_to_ASCII_from_greyscale_from_imageObject(im, output_file, cols, scale)

    return ascii_im

def main(argv):
    input_file = ""
    output_file = None
    columns = None
    scale = 0.43

    try:
        opts, _ = getopt.getopt(argv, "hi:o:cs", ["image=", "output=", "columns=", "scale="])
    except getopt.GetoptError:
        print("image_to_ASCII.py -i <image file name>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print("image_to_ASCII.py -i <image file name> -o <output file name> --columns <number of columns OPTIONAL> --scale <font scale OPTIONAL>")
            sys.exit()
        elif opt in ("-i", "--image"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg
        elif opt in "--columns":
            try: 
                columns = int(arg)
            except ValueError:
                columns = None
        elif opt in "--scale":
            try:
                scale = float(arg)
            except ValueError:
                scale = 0.43
    
    # Create ASCII art
    im = load_image(input_file)
    im = create_grayscale_image(im)
    convert_to_ASCII_from_greyscale_from_imageObject(im, output_file, columns, scale)
        
        
if __name__ == "__main__":
    main(sys.argv[1:])
