Image to ASCII art converter with support for consol and in code usage.

## In code usage
To create ASCII art from image file call `convert_to_ASCII_from_file`, to save it specify output file or grab returned string.

You can also create ASCII art from Image Pillow Object by calling `convert_to_ASCII_from_imageObject`.

If you want to specify the number of columns that your ASCII art will has, specify `columns` argument, by default it will be set as a horizontal number of pixels. 

If you are using specific font and you know scale of it, you can specify `scale` arguments, by default it is set as `0.43` and it is recommended.

## Terminal usage
In terminal type `image_to_ASCII.py` with obligatory arguments:
* `-i` input file name
* `-o` output file name


And with optional arguments:
* `--columns` number of columns that outputed ASCII art will has. By default is set as a horizontal number of pixels of an image.
* `--scale` scale of a font, default is set to 0.43
