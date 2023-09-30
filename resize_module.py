from PIL import Image

class Resize:
	def __init__(self):
		pass

	def resize(self, image, width_option, height_option, resize):
		resized_image = image
		width, height = image.size

		if width_option == True:
			new_width = resize
			new_height = new_width * height / width
		else:
			new_height = resize
			new_width = new_height * width / height

		resized_image = resized_image.resize((int(new_width), int(new_height)), Image.LANCZOS)

		return resized_image