import cv2  # Для работы с изображениями и видео
import numpy as np
from django.db.models.expressions import result
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import requests



orc=PaddleOCR() #Creating a PaddleOCR object for text recognition


class ImageHandler:
    """Class for working with images"""

    @staticmethod
    def open_image(img_path):
        """Opens an image and returns it in RGB format"""

        if img_path:
            response = requests.get(img_path)
            if response.status_code != 200:
                raise FileNotFoundError(f"Failed to download image from {img_path}")
            img_data=np.array(bytearray(response.content),dtype='uint8') #преобразуем изображение в масив Numpy
            car_plate=cv2.imdecode(img_data,cv2.IMREAD_COLOR)
        else:
            car_plate = cv2.imread(img_path)
        if car_plate is None:
            raise FileNotFoundError(f"Failed to open image from {img_path}")
        return cv2.cvtColor(car_plate, cv2.COLOR_BGR2RGB)


    @staticmethod
    def enlarge_image(img, scale_factor):
        """Enlarges the image by the specified percentage."""
        width = int(img.shape[1]*scale_factor/100)
        height = int(img.shape[0]*scale_factor/100)
        return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)


class CarPlateExtractor:
    """Class for extracting license plates from images"""
    def __init__(self, cascade_path):
        """Initializes the CascadeClassifier object for license plate detection."""
        self.classifier = cv2.CascadeClassifier(cascade_path)
        if not self.classifier.empty():
            print("License plate detection cascade classifier loaded successfully.")


    def extract(self,image):
        """Extracts license plates from an image"""
        carplate_rects=self.classifier.detectMultiScale(image,scaleFactor=1.04,minNeighbors=6, minSize=(30, 30))
        carplate_imgs = [image[y + 10:y + h - 5, x + 10:x + w - 5] for x, y, w, h in carplate_rects]
        return carplate_imgs

class OCRProcessor:
    """Class for performing OCR using PaddleOCR"""

    def __init__(self):
        """Initializes the PaddleOCR object for text recognition."""
        self.ocr = PaddleOCR()


    def process(self,image):
        """Performs OCR on an image and returns the recognized text."""
        result = self.ocr.ocr(image, cls=True)
        return result

class CarPlateRecognizer:
    """Class for recognition of license plates"""
    def __init__(self, classifier_path, font_path):
        self.extractor=CarPlateExtractor(classifier_path)
        self.ocr_processor=OCRProcessor()
        self.font_path=font_path


    def recognize(self,img_path):
        """Recognizes car numbers in an image"""

        try:
            img=ImageHandler.open_image(img_path)
            carplate_imgs=self.extractor.extract(img)

            if not carplate_imgs:
                print("No car numbers")
                return
            numbers = []
            for carplate_img in carplate_imgs:
                carplate_img=ImageHandler.enlarge_image(carplate_img,150)
                carplate_imgs=cv2.cvtColor(carplate_img,cv2.COLOR_BGR2GRAY)

                # img_to_show = Image.fromarray(carplate_img)
                # img_to_show.show()

                result=self.ocr_processor.process(carplate_imgs)

                if result:
                    for line in result[0]:
                        print(f"Recognized text: {line[1][0]} (Confidence: {line[1][1]:.2f})")
                        numbers.append(line[1][0])
                else:
                    print("OCR failed to recognize text.")
            return numbers
        except Exception as e:
         print(f"Error: {str(e)}")


if __name__ == "__main__":
    recognizer = CarPlateRecognizer(classifier_path='model/haarcascade_russian_plate_number.xml',
                                font_path='font/simfang.ttf')
    recognizer.recognize('cars/31-aa9922bb.jpg')











