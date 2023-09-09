import cv2

class PlateDetector():
    def __init__(self) -> None:
        self.__classifier = cv2.CascadeClassifier("src/computer_vision/haarcascade_russian_plate_number.xml")
        self.scaleFactor = 1.03
        self.minNeighbors = 7

    
    def detect(self, image_path: str) -> list:
        image = cv2.imread(image_path)
        return self.detect(image)
    
    def detect(self, image: cv2.typing.MatLike) -> list:
        if image is None:
            raise Exception("Could not read image")
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Detect plates
        detections = self.__classifier.detectMultiScale(gray, scaleFactor=self.scaleFactor, minNeighbors=self.minNeighbors)

        plates_coordinates = []

        # loop over the number plate bounding boxes
        for (x, y, w, h) in detections:
            # draw a rectangle around the number plate
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv2.putText(image, "Number plate detected", (x - 20, y - 10),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 2)

            # extract the number plate from the grayscale image
            plates_coordinates.append((x, y, w, h))
        
        return plates_coordinates

    def detect_and_show(self, image_path:str) -> list:
        image = cv2.imread(image_path)
        if image is None:
            raise Exception("Could not read image")
        coords = self.detect(image)

        # loop over the number plate bounding boxes
        for (x, y, w, h) in coords:
            # draw a rectangle around the number plate
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv2.putText(image, "Number plate detected", (x - 20, y - 10),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 2)

            # extract the number plate from the grayscale image
            # plates_coordinates.append((x, y, w, h))
        
        # resize the image for better display keeping the aspect ratio in mind
        # the maximum width of the image is set to 900 pixels
        width = image.shape[1]
        height = image.shape[0]
        max_width = 900
        if width > max_width:
            ratio = max_width / width
            height = int(height * ratio)
            image = cv2.resize(image, (max_width, height), interpolation=cv2.INTER_AREA)

        # show the output image
        cv2.imshow("Number plate detected", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        

