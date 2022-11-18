import cv2
# import รูป
original_image = cv2.imread('pic05.png')


# กรองให้เป็นขาวดำ เพื่อแยกจากพื้นหลัง
lower=(250,250,250)
upper=(255,255,255)
mask = cv2.inRange(original_image, lower, upper)
image = original_image.copy()
image[mask!=255] = (0, 0, 0)

#สร้างไฟล์เสมือนรูป
original = image.copy()



#นำขนาดของรูปมาแบ่งครึ่ง เพื่อแยกฝั่งซ้ายและขวา
image_h, image_w, image_c = image.shape


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
ROI_number = 0
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

#array สำหรับเก็บฝั่งซ้าย
files_right = []
files_left = []
x_location_left = []
y_location_left = []
x_lenght_location_left  = []
y_lenght_location_left  = []

#array สำหรับเก็บฝั่งขวา
x_location_right = []
y_location_right = []
x_lenght_location_right = []
y_lenght_location_right = []


for c in cnts:
    
    x,y,w,h = cv2.boundingRect(c)
    if w > 30:
        


        if x > image_w/2:
            x_location_right.append(x)
            y_location_right.append(y)
            y_lenght_location_right.append(y+h)
            x_lenght_location_right.append(x+w)
            
            #กำหนดขนาดที่ตายตัว สำหรับตัด
            w = 150
            h = 150
            
            #นำรูปมาตัด จากบรรทัดที่ 15
            ROI = original[y:y+h, x:x+w]
            cv2.imwrite('ROI_{}_right.png'.format(ROI_number), ROI)

            files_right.append('ROI_{}_right.png'.format(ROI_number))
            
        else:
            x_location_left.append(x)
            y_location_left.append(y)
            y_lenght_location_left.append(y+h)
            x_lenght_location_left.append(x+w)
            

            #กำหนดขนาดที่ตายตัว สำหรับตัด
            w = 150
            h = 150

            #นำรูปมาตัด จากบรรทัดที่ 15
            ROI = original[y:y+h, x:x+w]

            cv2.imwrite('ROI_{}_left.png'.format(ROI_number), ROI)

            files_left.append('ROI_{}_left.png'.format(ROI_number))
           
        ROI_number += 1



#สร้างสีที่แตกต่างสำหรับแต่ละคู่
def get_color(index):
    if index == 0:
        rgbl=[255,0,0]
    elif index == 1:
        rgbl=[0,255,0]
    elif index == 2:
        rgbl=[0,0,255]
    elif index == 3:
        rgbl=[255,255,0]
    elif index == 4:
        rgbl=[0,255,255]
    elif index == 5:
        rgbl=[255,0,255]
    elif index == 6:     
        rgbl=[70,255,30]
    return rgbl

    

i = 0
for left_name in files_left:
    
    template = cv2.imread(left_name, 0)

    high_score = []



    for name in files_right:
        img = cv2.imread(name, 0)

        #นำระดับความเหมือนมาเก็บเป็นคะแนน
        score = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED).max()

        high_score.append(score)

    

    #นำคะแนนความเหมือนที่ได้มาหาค่ามากที่สุด แล้วเอาไปใส่ใน id 
    files_right_id = int(files_right.index(files_right[high_score.index(max(high_score))]))
    left_name_id = int(files_left.index(left_name))
    
    #สร้างสี่เหลี่ยมฝั่งซ้าย
    cv2.rectangle(original_image, (x_location_left[left_name_id], y_location_left[left_name_id]), ( x_lenght_location_left[left_name_id], y_lenght_location_left[left_name_id]), (get_color(i)), 2)
    #สร้างสีเหลี่ยมฝั่งขวา
    cv2.rectangle(original_image, (x_location_right[files_right_id], y_location_right[files_right_id]), ( x_lenght_location_right[files_right_id], y_lenght_location_right[files_right_id]), (get_color(i)), 2)

    
    i += 1


cv2.imshow('image', original_image)
cv2.waitKey()
