class memoir:
    memoir_num = 0
    def __init__(self,my_univ, field, college, major,continent, country,ex_univ,semester,info):
        self.my_univ=my_univ
        self.field=field
        self.college=college
        self.major=major
        self.country=country
        self.continent=continent
        self.ex_univ=ex_univ
        self.semester=semester
        self.info=info
        memoir.memoir_num+=1
    
    def __str__(self):
        rep="my_univ: {}\nfield: {}\ncollege: {}\nmajor: {}\ncountry: {}\ncontinent: {}\nex_univ: {}\nsemester: {}\nurl:{}\nnum: {}".format(
        self.my_univ,self.field,self.college,self.major,self.country,self.continent,self.ex_univ,self.semester,self.info)
        
        return rep