# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

from PIL import Image, ImageDraw, ImageFont

import os
#import Watermark_module
import Exif_module

class Converter():
	def __init__(self) -> None:
		#self.watermark = Watermark_module.Watermark()
		self.exif = Exif_module.Exif()

	def ConvertImageToWebP(self, filePath, savePath, saveName, loselessOpt, imageQualityOpt, exifOpt, iccProfileOpt, exactOpt, watermarkText, exifViewOpt, conversionOpt):
		condition, fileFormat = self.SearchFileFormat(filePath)

		if condition:
			# 01 일반 WebP 형식 Image로 변환할 때
			if conversionOpt == True:
				image = Image.open(filePath).convert('RGB')

				filePath = filePath.replace(fileFormat, '.webp')
				dest = savePath+saveName+".webp"
				
				exifData = getattr(image.info, 'exif', None)
				if not exifData:
					print(f'no exif data {saveName}')
					exifOpt = False

				iccProfile = image.info['icc_profile']
			
				#image = self.watermark.InsertWatermark(image=image, fontColor=watermarkColor, watermarkText=watermarkText)

				if exifOpt == True:
					if iccProfileOpt == True:
						image.save(dest, format="webp", loseless=loselessOpt, quality=imageQualityOpt, exif=exifData, exact = exactOpt, icc_profile=iccProfile)
					else:
						image.save(dest, format="webp", loseless=loselessOpt, quality=imageQualityOpt, exif=exifData, exact = exactOpt)

				else:
					if iccProfileOpt == True:
						image.save(dest, format="webp", loseless=loselessOpt, quality=imageQualityOpt, exact=exactOpt, icc_profile=iccProfile)
					else:
						image.save(dest, format="webp", loseless=loselessOpt, quality=imageQualityOpt, exact=exactOpt)

	def ConvertExifImage(self, filePath, savePath, saveName, fileFormatOpt):
		condition, fileFormat = self.SearchFileFormat(filePath)

		if condition:
			# 02 EXIF Padding Image로 변환할 때
			image = Image.open(filePath)

			longerLength = image.width if image.width >= image.height else image.height
			padding = int(longerLength / 10)

			modelData, exifData = self.exif.GetExifData(image)

			image = self.exif.SetImagePadding2(image, top=int(padding/2), side=int(padding/2), bottom=padding, color=(255,255,255))
			image = self.exif.SetImageText(image, modelData=modelData, exifData=exifData, length = padding)

			# 파일 형식 선택
			if fileFormatOpt == 0:
				dest = savePath+saveName+'.jpeg'
				image.save(dest, format='jpeg')
			elif fileFormatOpt == 1:
				dest = savePath+saveName+'.png'
				image.save(dest, format='png')
			elif fileFormatOpt == 2:
				dest = savePath+saveName+'.webp'
				image.save(dest, format='webp', quality=92)
			else:
				print("잘못된 파일 변환 선택지 입니다.")
				return

		else:
			print("잘못된 파일 형식 입니다.")
			return

	def SearchFileFormat(self, filePath):
		fileFormat = os.path.splitext(filePath)[1]
		if(fileFormat == ".jpg" or fileFormat == ".jpeg" or fileFormat == ".png" or fileFormat == ".tiff"):
			return True, fileFormat
		else:
			return False, None