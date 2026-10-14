# initiate the databas 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum 
import uuid
# create its variable 
db = SQLAlchemy()

# define all enumns 
class DepartmentType(enum.Enum):
    PRODUCTION = "Production"
    LABORATORY  = "Laboratory"
    MAINTENANCE = "Maintenance"
    QUALITY_ASSURANCE = "Quality Assurance"
    RESEARCH_AND_DEVELOPMENT = "Research & Development"
    UTILITIES = "Utilities"
    HEALTH_AND_SAFETY = "Health & Safety"

class ShiftType(enum.Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    NIGHT = "Night"

class SeverityType(enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = 'High'
    CRITICAL = "Critical"

class HazardType(enum.Enum):
    FLAMMABLE = 'Flammable'
    CORROSIVE = 'Corrosive'
    TOXIC = "Toxic"
    OXIDIZING = "Oxidizing"
    REACTIVE = "Reactive"
    ENVIRONMENTAL_HAZARD = "Environmental Hazard"

class PositionType(enum.Enum):
    PROCESS_OPERATOR = "Process Operator"
    SHIFT_SUPERVISOR = "Shift Supervisor"
    SAFETY_OFFICER = "Safety Officer"
    LABORATORY_TECHNICIAN = "Laboratory Technician"
    MAINTENANCE_ENGINEER = "Maintenance Engineer"

#create a function to generate employee id  
def generate_employee_id():
    return f"EMP-{uuid.uuid4().hex[:4].upper()}"

# create the operators model
class Operator(db.Model):
    __tablename__ = 'operators'

    id  = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), nullable=False, unique=True, default=generate_employee_id)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    department = db.Column(db.Enum(DepartmentType), nullable=False)
    position = db.Column(db.Enum(PositionType), nullable=False)
    shift =  db.Column(db.Enum(ShiftType), nullable=False, default=ShiftType.MORNING)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    reports = db.relationship("Report", back_populates='operator')

    # how to diplay the operators 
    def __repr__(self):
        return f"<{self.employee_id} - {self.email} - {self.department.value}>"


# create the chemical model
class Chemical(db.Model):
    __tablename__ = "chemicals"

    id = db.Column(db.Integer, primary_key=True)
    chemical_name = db.Column(db.String(100), nullable=False)
    cas_number = db.Column(db.String(100), unique=True, nullable=False)
    hazard_class = db.Column(db.Enum(HazardType), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    reports = db.relationship("Report", back_populates='chemical')

    def __repr__(self):
        return f"<{self.chemical_name} - {self.cas_number}>"


# create the inventory model 
class IncidentType(db.Model):
    __tablename__ = "incident_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reports = db.relationship('Report', back_populates='incident_type')
    predicted_analyses = db.relationship('ReportAnalysis', back_populates="predicted_incident_type")

    def __repr__(self):
        return f"<{self.name} - {self.description}>"


# creating the reports table that connects to all other tables 
class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, )
    operator_id = db.Column(db.Integer, db.ForeignKey("operators.id"), nullable=False)
    chemical_id = db.Column(db.Integer, db.ForeignKey("chemicals.id"), nullable=False)
    incident_type_id = db.Column(db.Integer, db.ForeignKey("incident_types.id"), nullable=False)
    severity = db.Column(db.Enum(SeverityType), nullable=False)
    location = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    operator = db.relationship("Operator", back_populates='reports')
    chemical = db.relationship('Chemical', back_populates='reports')
    incident_type = db.relationship("IncidentType", back_populates='reports')
    report_analysis = db.relationship("ReportAnalysis", back_populates='report', uselist=False)

    def __repr__(self):
        return f"<{self.title} - {self.severity.value}>"


# create the model prediction table of the result
class ReportAnalysis(db.Model):
    __tablename__ = "report_analysis"

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey("reports.id"), nullable=False, unique=True)
    predicted_incident_type_id = db.Column(db.Integer, db.ForeignKey("incident_types.id"), nullable=True)
    confidence_score = db.Column(db.Float, nullable=False)
    model_version = db.Column(db.String(100), nullable=False)
    analysed_at = db.Column(db.DateTime, default=datetime.now)
    report = db.relationship('Report', back_populates='report_analysis')
    predicted_incident_type = db.relationship("IncidentType", back_populates='predicted_analyses')



    def __repr__(self):
        return f"<{self.report_id} - {self.predicted_incident_type_id} - {self.confidence_score} - {self.model_version}>"

