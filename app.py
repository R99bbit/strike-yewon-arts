from selenium import webdriver
from selenium.webdriver.support.ui import Select
import chromedriver_autoinstaller
import time
import threading

from ttk import *
from tkinter import *
import tkinter.messagebox

class StrikeYewonArtsModel:
    def __init__(self, curri_code_key, younggb_key, grade_key, juya_key, hakbu_code_key, gwa_key, lecture_name, id, pw):
        ''' install chrome driver and apply to local system '''
        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인

        try:
            driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')   
        except:
            chromedriver_autoinstaller.install('./')
            driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')

        driver.implicitly_wait(1)
        self.driver = driver

        ''' load login information '''
        self.id = id
        self.pw = pw

        ''' load lecture information '''
        self.curri_code_key = curri_code_key
        self.younggb_key = younggb_key
        self.grade_key = grade_key
        self.juya_key = juya_key
        self.hakbu_code_key = hakbu_code_key
        self.gwa_key = gwa_key
        self.lecture_name = lecture_name

        self.curri_code = { # 구분
            '교양필수' : '11',
            '교양선택' : '12',
            '교양' : '13',
            '전공필수' : '21',
            '전공선택' : '22',
            '자유선택' : '31',
            '계열기초' : '41',
            '교직' : '81',
            '전공기초' : '44',
            '전공심화' : '23',
            '전공인정' : '24',
            '계열선택' : '25'
        }

        self.younggb = { # 영역(교필, 교선, 교양만 해당, 이외 항목에서 선택하지 않도록 FORCE)
            '1영역' : '05100057', # 1영역(기초예술)
            '2영역' : '05100051', # 2영역(인문과 역사)
            '3영역' : '05100052', # 3영역(언어와 생활)
            '4영역' : '05100053', # 4영역(콘텐츠와 표현)
            '5영역' : '05100054', # 5영역(과학과 기술경영)
            '6영역' : '05100058', # 6영역(취업과 창업)
            '7영역' : '05100059', # 7영역(건강과 사회봉사)
            '8영역' : '05100060'  # 8영역(문화예술교육사)
        }

        self.grade = { # 학년
            '1학년' : '1',
            '2학년' : '2',
            '3학년' : '3',
            '4학년' : '4',
            '5학년' : '5'
        }

        self.juya = { # 주간/야간
            '주간' : '주',
            '야간' : '야'
        }

        self.hakbu_code = { # 학부
            '문화재보존예술학과' : 'H01401',
            '문화예술관광콘텐츠학과' : 'H01402',
            '미술/디자인학부' : 'H01001',
            '만화/게임영상학부' : 'H01004',
            '음악학과' : 'H01105',
            '무용학과1' : 'H01106',
            '교양학부' : 'H01099',
            '공연ㆍ음악학부' : 'H01013',
            '스포츠레저복지학부' : 'H01014',
            '미술조형학과' : 'H01301',
            '애니메이션학과' : 'H01303',
            '미디어예술학과' : 'H01304',
            '시각디자인학과' : 'H01302',
            '경호무도학과' : 'H01305',
            '문화재/보존학과' : 'H02004',
            '글로벌호텔관광경영학과' : 'H02102',
            '호텔관광경영학과' : 'H02103',
            '문화재/관광학부' : 'H02003',
            '스포츠학과' : 'H05007',
            '음악학과' : 'H01207',
            '한지조형디자인학과' : 'H01201',
            '스포츠복지학부' : 'H01015',
            '귀금속보석디자인학과' : 'H01202',
            '만화게임영상학과' : 'H01203',
            '연극영화ㆍ코미디학과' : 'H01204',
            '실용음악학과' : 'H01205',
            '뮤지컬학과' : 'H01206',
            '생활체육학과' : 'H01208',
            '무용학과' : 'H01209',
            '뷰티패션디자인학과' : 'H01018',
            '연극영화학과' : 'H01210',
            '한지공간조형디자인학과' : 'H01306',
            '금속조형디자인학과' : 'H01307',
            '공연예술뮤지컬학과' : 'H01308',
            '미술조형디자인학부' : 'H01309',
            '미술조형디자인학부' : 'H01310',
            '디지털콘텐츠학부' : 'H01311',
            '디지털콘텐츠학부' : 'H01312',
            '공연예술학부' : 'H01313',
            '공연예술학부' : 'H01314',
            '스포츠경호무도학과' : 'H01315'
        }

        # 학과는 직접 입력

    def accessYewonArtsAU(self):
        ''' access to yewon arts au - login.jsp '''
        self.driver.get('http://webedu.yewon.ac.kr/yewon/schoolaffairs/haksa_login.jsp')

    def getUserCertification(self, id, pw):
        ''' find login form and input user cert '''
        self.driver.find_element_by_name('hakbun').send_keys(id)
        self.driver.find_element_by_name('secr').send_keys(pw)
        self.driver.find_element_by_name('Submit').click()

    def gotoLectureFrame(self):
        ''' goto lecture frame '''
        self.driver.get('http://webedu.yewon.ac.kr/yewon/schoolaffairs/lecture/lecture_frame.jsp')
        self.driver.get('http://webedu.yewon.ac.kr/yewon/schoolaffairs/lesson/lesson_list.jsp?op=src&sessionId=')
        self.driver.refresh()

    def setCategory(self, curri_code, younggb, grade, juya, hakbu_code, gwa):
        ''' set category and search '''
        Select(self.driver.find_element_by_name('findcurri_code')).select_by_value(curri_code) # 구분
        Select(self.driver.find_element_by_name('findyounggb')).select_by_value(younggb) # 영역 / 구분에 따라 있고 없고
        Select(self.driver.find_element_by_name('findgrade')).select_by_value(grade) # 학년
        Select(self.driver.find_element_by_name('findjuya')).select_by_value(juya) # 주/야
        Select(self.driver.find_element_by_name('findhakbu_code')).select_by_value(hakbu_code) # 학부코드
        Select(self.driver.find_element_by_name('findgwa_code')).select_by_visible_text(gwa) # 학과코드

        self.driver.find_element_by_xpath('//input[@type="image"]').click()

    def submitLectureRequest(self, lecture_name):
        ''' submit lecture '''
        self.driver.find_element_by_xpath(f"//*[contains(text(), '{lecture_name}')]").find_element_by_xpath('..').find_element_by_tag_name('a').click()

    def run(self):
        self.accessYewonArtsAU()
        self.getUserCertification(self.id, self.pw)
        self.gotoLectureFrame()

        self.setCategory(
            self.curri_code[self.curri_code_key], 
            self.younggb[self.younggb_key], 
            self.grade[self.grade_key], 
            self.juya[self.juya_key], 
            self.hakbu_code[self.hakbu_code_key], 
            self.gwa_key
        )

        self.submitLectureRequest(self.lecture_name)
        time.sleep(0.5)
        self.driver.quit()

class LoginGUI:
    def __init__(self):
        def submit():
            _id = str(id_entry.get())
            _pw = str(pw_entry.get())
            if (_id == "") or (_pw == ""):
                tkinter.messagebox.showwarning("경고는 월닝", "학번 또는 암호가 입력되지 않았습니다.")
                return

            global input_id 
            global input_pw 

            input_id = _id
            input_pw = _pw
            
            tkinter.messagebox.showinfo("로그인 성공", "아래 계정으로 설정되었습니다.\n학번 : " + input_id + "\n암호 : " + input_pw)
            root.destroy()

        root = Tk()
        root.title('Strike Yewon - 로그인')
        root.geometry("230x70")
        root.resizable(False, False)

        id_lbl = Label(root, text="학번 : ", anchor=CENTER)
        id_lbl.grid(row=0, column=0)

        id_entry = Entry(root, width=20)
        id_entry.grid(row=0, column=1)
        
        pw_lbl = Label(root, text="암호 : ", anchor=CENTER)
        pw_lbl.grid(row=1, column=0)

        pw_entry = Entry(root, width=20)
        pw_entry.grid(row=1, column=1)

        alert_lbl=Label(root, text="※ 버그 문의는 받지 않습니다. 귀찮아용")
        alert_lbl.grid(row=2, column=0, columnspan=2)
        
        submit_btn = Button(root, command=submit, text='로그인')
        submit_btn.grid(row=0, column=2, columnspan=2, rowspan=2)

        root.mainloop()


class LectureManagementGUI():
    def __init__(self):
        root=Tk()
        root.title('Strike Yewon - 장바구니')
        root.geometry("560x300")
        root.resizable(False, False)
        
        ''' 구분 '''
        curri_code_lbl = Label(root, text="구분 : ")
        curri_code_lbl.grid(row=0, column=0)

        choices1 = ['교양필수', '교양선택', '교양', '전공필수', '전공선택', '자유선택', '계열기초', '교직', '전공기초', '전공심화', '전공인정', '계열선택']
        curri_code_combo = Combobox(root, values = choices1, width=10)
        curri_code_combo.grid(row=0, column=1, pady=15)
        '''      '''

        ''' 영역 '''
        younggb_lbl = Label(root, text="영역 : ")
        younggb_lbl.grid(row=0, column=2)

        choices2 = ['1영역', '2영역', '3영역']
        
        younggb_combo = Combobox(root, values = choices2, width=10)
        younggb_combo.grid(row=0, column=3)
        '''      '''

        ''' 학년 '''
        grade_lbl = Label(root, text="학년 : ")
        grade_lbl.grid(row=0, column=4)

        choices3 = ['1학년', '2학년', '3학년', '4학년', '5학년']

        grade_combo = Combobox(root, values=choices3, width=10)
        grade_combo.grid(row=0, column=5)
        '''      '''

        ''' 주야 '''
        juya_lbl = Label(root, text="    주/야 : ")
        juya_lbl.grid(row=0, column=6)

        choices4 = ['주간', '야간']

        juya_combo = Combobox(root, values=choices4, width=10)
        juya_combo.grid(row=0, column=7)
        '''      '''

        ''' 학부 '''
        hakbu_code_lbl = Label(root, text="학부 : ")
        hakbu_code_lbl.grid(row=1, column=0)

        choices5 = ['교양학부', '컴퓨터융합학부']

        hakbu_code_combo = Combobox(root, values=choices5, width=10)
        hakbu_code_combo.grid(row=1, column=1, pady=10)
        '''      '''

        ''' 학과 '''
        gwa_lbl = Label(root, text="학과 : ")
        gwa_lbl.grid(row=1, column=2)

        gwa_entry = Entry(root, width=12)
        gwa_entry.grid(row=1, column=3)
        '''      '''

        
        ''' 과목 '''
        lecture_lbl = Label(root, text="과목 : ")
        lecture_lbl.grid(row=1, column=4)
        
        lecture_entry = Entry(root, width=20)
        lecture_entry.grid(row=1, column=5, columnspan=2)
        '''      '''

        ''' 추가 버튼 '''
        def add_to_listbox():
            all_combo_info = [curri_code_combo.get(), younggb_combo.get(), grade_combo.get(), juya_combo.get(), hakbu_code_combo.get(), gwa_entry.get(), lecture_entry.get()]
            listbox.insert("end", all_combo_info)
            lecture_info_list.append(all_combo_info)
            print(lecture_info_list)
            print(len(lecture_info_list))
        add_btn = Button(root, command=add_to_listbox, text="추가!", width=8)
        add_btn.grid(row=1, column=7)
        '''           '''


        ''' 장바구니 '''
        ex_lbl = Label(root, text="신청목록(구분 / 영역 / 학년 / 주야 / 학부 / 전공 / 강의명)")
        ex_lbl.grid(row=2, column=1, columnspan=5, sticky="nsew", pady=10)
        listbox = tkinter.Listbox(root, selectmode='extended', height=0, width=50)
        listbox.insert("end", ['교양', '2영역', '1학년', '주간', '교양학부', '교양학부', '동양미술사의 이해와 감상'])

        listbox.grid(row=3, column=1, columnspan=5, sticky="nsew", padx=10)
        '''          '''

        ''' Fight 버튼 '''
        def fight_():
            root.destroy()
        fight_btn = Button(root, command=fight_, text="FIGHT!")
        fight_btn.grid(row=3, column=6, sticky="nsew")

        ''' Delete 버튼 '''
        def delete_list():
            listbox.delete("end")
            lecture_info_list.pop()
        delete_btn = Button(root, command=delete_list, text="DELETE", height=6)
        delete_btn.grid(row=3, column=7)
    
        root.mainloop()


''' global variable '''
input_id = ""
input_pw = ""
lecture_info_list = []

if __name__ == "__main__":
    login_gui = LoginGUI() # 20180157 !000129
    print("ID :", input_id)
    print("PW :", input_pw)
    
    lecture_gui = LectureManagementGUI()
    for i in range(len(lecture_info_list)):
        print(lecture_info_list[i][1])
        model = StrikeYewonArtsModel(lecture_info_list[i][0], lecture_info_list[i][1], lecture_info_list[i][2], lecture_info_list[i][3], lecture_info_list[i][4], lecture_info_list[i][5], lecture_info_list[i][6], input_id, input_pw)
        model.run()

    # Model(self, curri_code_key, younggb_key, grade_key, juya_key, hakbu_code_key, gwa_key, lecture_name, id, pw)
    # model = StrikeYewonArtsModel('교양', '2영역', '1학년', '주간', '교양학부', '교양학부', '동양미술사의 이해와 감상', input_id, input_pw)
    # model.run()
    
