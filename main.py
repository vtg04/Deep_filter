import cv2
import dlib
import face_recognition

# Load pre-trained models for dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Load the reference image and get face encodings
reference_image = face_recognition.load_image_file('elon_musk.jpg')  # Use 'cristiano_ronaldo.jpg' for Ronaldo
reference_face_encoding = face_recognition.face_encodings(reference_image)[0]

# Function to apply the deepfake filter
def apply_deepfake_filter(frame, reference_face_encoding):
    # Convert the frame to RGB (required by face_recognition)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all the faces and face encodings in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare face encodings
        matches = face_recognition.compare_faces([reference_face_encoding], face_encoding)

        if True in matches:
            # If there's a match, swap faces
            # Placeholder for actual face swapping code
            # You'd use cv2.seamlessClone() or similar techniques here
            frame[top:bottom, left:right] = reference_image[0:(bottom-top), 0:(right-left)]

    return frame

# Open the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply the deepfake filter to the frame
    frame = apply_deepfake_filter(frame, reference_face_encoding)

    # Display the frame
    cv2.imshow('Deepfake Filter', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
