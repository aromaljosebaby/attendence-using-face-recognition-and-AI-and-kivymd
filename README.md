# attendence-using-face-recognition-and-AI-and-kivymd
A project which automates the process of taking attendence using face recognition and AI and designed using kivymd gui



Steps to follow before installing the required packages and running the code:


1) After installing cmake you have to install the C++ package from visual studio site
https://visualstudio.microsoft.com/downloads/?utm_medium=microsoft&utm_source=docs.microsoft.com&utm_campaign=button+cta&utm_content=download+vs2019+rc


2) For more information n dlib installation  reffer https://www.youtube.com/watch?v=D5xqcGk6LEc


3) Make sure you first train images to recognize before starting the attendence process

4) To quit from the attendence portal press q 


How the code works:

  The images you train go to the folder Train Images,this will be the image of the students you want to recognize.

  Note: Dont directly add student images to Train Images , but use the feature add image in the home page,because this image is stored ina specific format with the roll number of   the student.

  The attendence register will be stored as a csv file in the folder AttendenceRegister with the corresponding days date.

  The attendence register contains the students name and the time in which the student enterd the attendence system.

