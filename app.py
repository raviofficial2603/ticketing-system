from flask import Flask,render_template,request
import uuid,json
app = Flask(__name__)
class Employee:
    
    def __init__(self,id,name,tickets) -> None:
        self.id=id
        self.name=name
        self.tickets=tickets
    def __str__(self) -> str:
        return 'id='+str(self.id)+" name="+self.name
    

class Ticket:
    
    def __init__(self,id,issue_description,assigned_to,raised_by) -> None:
        self.ticket_id=id
        self.assigned_to=assigned_to
        self.issue_description=issue_description
        self.raised_by=raised_by
    def __str__(self) -> str:
        return "id="+str(self.id)+" assigned_to="+self.assigned_to+"issue_description="+self.issue_description+" raised_by="+self.raised_by
        

class RoundRobinQueue:
    def __init__(self, employees):
        self.employees = employees
        self.current_index = 0

    def get_next_employee(self):
        if not self.employees:
            return None

        employee = self.employees[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.employees)
        return employee

ticket1=Ticket(uuid.uuid1(),'My teams app is not working properly',1,5)
ticket2=Ticket(uuid.uuid1(),'My outlook app is not working properly',2,4)
ticket3=Ticket(uuid.uuid1(),'Not able to login',3,5)
ticket4=Ticket(uuid.uuid1(),'Not able to run more than one appplication',4,2)
ticket5=Ticket(uuid.uuid1(),'Flask is not getting installed',5,1)
emp1=Employee(1,'Ramesh',[ticket1])        
emp2=Employee(2,'Suresh',[ticket2])
emp3=Employee(3,'Harish',[ticket3])
emp4=Employee(4,'Krishna',[ticket4])
emp5=Employee(5,'Srinivas',[ticket5])
emp_list=[emp1,emp2,emp3,emp4,emp5]
rr=RoundRobinQueue(emp_list)
ticket_list=[ticket1,ticket2,ticket3,ticket4,ticket5]

@app.route("/")
def welcome():
    return render_template("index.html",emp1=emp1,emp2=emp2,emp3=emp3,emp4=emp4,emp5=emp5)
@app.route("/ticket", methods=['POST'])
def ticket():
    if request.method == 'POST':
        user_id = request.form['user_id']
        issue = request.form['issue_description'] 
        employee=rr.get_next_employee()
        ticket=Ticket(str(uuid.uuid1()),issue,employee.id,user_id) 
        ticket_list.append(ticket)  
        employee.tickets.append(ticket)
        return json.dumps({'message':"No Errors!!",'success':True,'data':{'ticket_id':ticket.ticket_id,'assigned_to':ticket.assigned_to}}) 



        
if __name__ == "__main__":
    
    app.debug = True
    app.run(host='0.0.0.0') 