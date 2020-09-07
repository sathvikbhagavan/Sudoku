from imutils.perspective import four_point_transform
import tensorflow as tf
from skimage.segmentation import clear_border
import numpy as np
import imutils
import cv2
import numpy as np
import argparse

# Finding the outline of the sudoku puzzle
def find_puzzle(image, debug=False):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (7, 7), 3)
	thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	thresh = cv2.bitwise_not(thresh)
	if debug:
		cv2.imshow("Puzzle Thresh", thresh)
		cv2.waitKey(0)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
	puzzle_cnt = None
	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		if len(approx) == 4:
			puzzle_cnt = approx
			break
	if puzzle_cnt is None:
		raise Exception(("Could not find Sudoku puzzle outline. "
			"Try debugging your thresholding and contour steps."))
	if debug:
		output = image.copy()
		cv2.drawContours(output, [puzzle_cnt], -1, (0, 255, 0), 2)
		cv2.imshow("Puzzle Outline", output)
		cv2.waitKey(0)
	puzzle = four_point_transform(image, puzzle_cnt.reshape(4, 2))
	warped = four_point_transform(gray, puzzle_cnt.reshape(4, 2))
	if debug:
		cv2.imshow("Puzzle Transform", puzzle)
		cv2.waitKey(0)
	return (puzzle, warped)


# Extracting each digit from the found grid
def extract_digit(cell, debug=False):
	thresh = cv2.threshold(cell, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	thresh = clear_border(thresh)
	if debug:
		cv2.imshow("Cell Thresh", thresh)
		cv2.waitKey(0)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	if len(cnts) == 0:
		return None
	c = max(cnts, key=cv2.contourArea)
	mask = np.zeros(thresh.shape, dtype="uint8")
	cv2.drawContours(mask, [c], -1, 255, -1)
	(h, w) = thresh.shape
	percent_filled = cv2.countNonZero(mask) / float(w * h)
	if percent_filled < 0.03:
		return None
	digit = cv2.bitwise_and(thresh, thresh, mask=mask)
	if debug:
		cv2.imshow("Digit", digit)
		cv2.waitKey(0)
	return digit


# Main calling function
# Once the digits are found, using ocr for classifying the digits
def get_grid(image_path, model_path, number_of_models, debug):
	print("[INFO] loading digit classifier...")
	models = []
	for i in range(number_of_models):
		models.append(tf.keras.models.load_model(model_path + str(i) + '.h5'))
	print("[INFO] processing image...")
	image = cv2.imread(image_path)
	image = imutils.resize(image, width=600)
	(puzzle_image, warped) = find_puzzle(image, debug)
	board = np.zeros((9, 9), dtype="int")
	step_x = warped.shape[1] // 9
	step_y = warped.shape[0] // 9
	cell_locs = []
	for y in range(0, 9):
		row = []
		for x in range(0, 9):
			start_x = x * step_x
			start_y = y * step_y
			end_x = (x + 1) * step_x
			end_y = (y + 1) * step_y
			row.append((start_x, start_y, end_x, end_y))
			cell = warped[start_y:end_y, start_x:end_x]
			digit = extract_digit(cell, debug)
			if digit is not None:
				roi = cv2.resize(digit, (28, 28))
				roi = roi.astype("float") / 255.0
				roi = tf.keras.preprocessing.image.img_to_array(roi)
				roi = np.expand_dims(roi, axis=0)
				pred = np.zeros((1, 10))
				for i in range(number_of_models):
					pred += models[i].predict(roi)
				pred = pred.argmax(axis=1)[0]
				print(pred)
				board[y, x] = pred
		cell_locs.append(row)
	print("[INFO] OCR'd Sudoku board:")
	return board
