import timetable.models as ttm
from django.http import HttpResponse
from django.shortcuts import render,redirect
import random as rnd


NUMB_OF_ELITE_SCHEDULES=1
TOURNAMENT_SELECTION_SIZE=3
MUTATION_RATE=0.1
POPULATION_SIZE=10


class Data:
    def __init__(self):
        self._rooms=[]
        self._meetingTimes=[]
        self._instructor=[]
        self._course=[]
        self._depts=[]
        self._numberOfClasses=0
        for i in ttm.Rooms.objects.all():
            self._rooms.append(i)
        for i in ttm.Instructor.objects.all():
            self._instructor.append(i)
        for i in ttm.MeetTime.objects.all():
            self._meetingTimes.append(i)
        for i in ttm.Course.objects.all():
            self._course.append(i)
        for i in ttm.Dept.objects.all():
            self._depts.append(i)
        self._numberOfClasses=len(self._course)
    def get_room(self):return self._rooms
    def get_instructor(self):return self._instructor
    def get_course(self): return self._course
    def get_dept(self): return self._depts
    def get_meetingTime(self):return self._meetingTimes
    def get_numberOfClasses(self): return self._numberOfClasses
class Class:
    def __init__(self,id,dept,course):
        self._id=id
        self._dept=dept
        self._course=course
        self._instructor=None
        self._meetingTime=None
        self._room=None
    def get_id(self): return self._id
    def get_dept(self):return self._dept
    def get_course(self): return self._course
    def get_room(self): return self._room
    def get_instructor(self): return self._instructor
    def get_meetingTime(self): return self._meetingTime
    def set_instructor(self,instructor):self._instructor=instructor
    def set_meetingTime(self,meetingTime):self._meetingTime=meetingTime
    def set_room(self,room):self._room=room
    def __str__(self):
        return str(self._dept.name_D)+","+str(self._course)+","+\
                str(self._room)+","+ str(self._instructor)+","+str(self._meetingTime)
data=Data()
class Schedule:
    def __init__(self):
        self._data=data
        self._classes=[]
        self._numbOfConflicts=0
        self._fitness=-1
        self._classNumb=0
        self._isFitnessChanged=True
    def initialize(self):
        
        depts=self._data.get_dept()
        for i in range(0,len(depts)):
            courses=depts[i].course.all()
            for j in range(0,len(courses)):
                newClass=Class(self._classNumb,depts[i],courses[j])
                self._classNumb+=1
                newClass.set_meetingTime(self._data.get_meetingTime()[rnd.randrange(0,len(data.get_meetingTime()))])
                newClass.set_room(data.get_room()[rnd.randrange(0,len(data.get_room()))])
                newClass.set_instructor(courses[j].ins.all()[rnd.randrange(0,len(courses[j].ins.all()))])
                self._classes.append(newClass)
        return self
    def get_classes(self):
        self._isFitnessChanged=True
        return self._classes
    def get_numOfConflicts(self): return self._numbOfConflicts
    def get_fitness(self):
        if(self._isFitnessChanged==True):
            self._fitness=self.calculate_fitness()
            self._isFitnessChanged=False
        return self._fitness
    
    #----
    def calculate_fitness(self):
        self._numbOfConflicts=0
        classes=self.get_classes()
        for i in range(0,len(classes)):
            if(classes[i].get_room().seatingCapacity<classes[i].get_course().maxStd):
                self._numbOfConflicts+=1
            for j in range(0,len(classes)):
                if(j>=i):
                    if(classes[i].get_meetingTime()==classes[j].get_meetingTime() and classes[i].get_id() != classes[j].get_id()):
                        if(classes[i].get_room() == classes[j].get_room()):
                            self._numbOfConflicts+=1
                        if(classes[i].get_instructor() == classes[j].get_instructor()):
                            self._numbOfConflicts+=1
        return 1/((1.0*self._numbOfConflicts+1))
    def __str__(self):
        returnValue=""
        for i in range(0,len(self._classes)-1):
            returnValue+=str(self._classes[i]+",")
        returnValue+=str(self._classes[len(self._classes)-1])
        return returnValue
class Population:
    def __init__(self,size):
        self._size=size
        self._data=data
        self._schedules=[]
        for i in range(0,size):
            self._schedules.append(Schedule().initialize())
    def get_schedules(self):return self._schedules
class GA:
    #đánh giá
    def evolve(self,population):
        return self._mutate_population(self._crossover_population(population))
    def _crossover_population(self,pop):
        crossover_pop=Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i=NUMB_OF_ELITE_SCHEDULES
        while i<POPULATION_SIZE:
            schedule1=self._select_tournament_population(pop).get_schedules()[0]
            schedule2=self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1,schedule2))
            i+=1
        return crossover_pop
    def _mutate_population(self,population):
        for i in range(NUMB_OF_ELITE_SCHEDULES,POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
    
        return population
    def _mutate_schedule(self,mutateSchedule):
        schedule=Schedule().initialize()
        for i in range(0,len(mutateSchedule.get_classes())):
            if (MUTATION_RATE>rnd.random()):
                mutateSchedule.get_classes()[i]=schedule.get_classes()[i]
        return mutateSchedule
    def _crossover_schedule(self,schedule1,schedule2):
        crossoverShedule=Schedule().initialize()
        for i in range(0,len(crossoverShedule.get_classes())):
            if(rnd.random()>0.5):
                crossoverShedule.get_classes()[i]=schedule1.get_classes()[i]
            else:
                crossoverShedule.get_classes()[i]=schedule2.get_classes()[i]
        return crossoverShedule
    def _select_tournament_population(self,pop):
        tournament_pop=Population(0)
        i=0
        while i <TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0,POPULATION_SIZE)])
            i+=1
        tournament_pop.get_schedules().sort(key=lambda x:x.get_fitness(),reverse=True)
        return tournament_pop

def get_data(tkb):
    data=Data()
    classes = tkb.get_classes()
    list_thu=['T2','T3','T4','T5','T6','T7','CN']
    list_Ca=['Ca1','Ca2','Ca3','Ca4']
    week=[]
    for i in range(len(list_thu)):
        day=[]
        for k in range(0,len(list_Ca)):
         
            for j in range(0,len(classes)):
                
                time=classes[j].get_meetingTime().time
                if list_thu[i] in time and list_Ca[k] in time:
                    enty=ttm.Enty()
                    enty.name_C=classes[j].get_course().name_C
                    enty.name_I=classes[j].get_instructor().name
                    enty.Romm_number=classes[j].get_room().number
                    enty.Thu=list_thu[i]
                    enty.Ca=list_Ca[k]
                    day.append(enty)
                else:
                    day=day
                
            
        week.append(day)
                
   
    return week

def test(request):
    global data
    data=Data()
    depts=data.get_dept()
    generationNUm=0
    courses=depts[0].course.all()
    x=Schedule()
    x.initialize()
    population=Population(POPULATION_SIZE)
    population.get_schedules().sort(key=lambda x:x.get_fitness(),reverse=True)
    schedule=population.get_schedules()[0]
    gen=GA()
    while (population.get_schedules()[0].get_fitness() != 1.0):
        generationNUm+=1
        population=gen.evolve(population)
        population.get_schedules().sort(key=lambda x:x.get_fitness(),reverse=True)
        out=population.get_schedules()[0]

    classes=out.get_classes()
    i=1
    r1=str(i)
    r2=classes[i].get_dept().name_D
    r3=classes[i].get_course().name_C+" ( "+ str(classes[i].get_course().maxStd)+")"
    r4=classes[i].get_room().number+"("+str(classes[i].get_room().seatingCapacity)+")"
    r5= classes[i].get_instructor().name
    r6=classes[i].get_meetingTime().time
    #return HttpResponse(r1+"\t"+r2+"\t"+r3+"\t"+r4+"\t"+r5+"\t"+r6+"\t"+"\t"+str(len(classes)))
    w=get_data(out)
    #return HttpResponse("\t"+str(len(w[6])))
    

    return render(request,"show_tkb.html",{'weeks':w})