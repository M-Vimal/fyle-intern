import enum
from flask import abort
from core import db
from core.apis.decorators import AuthPrincipal
from core.libs import helpers, assertions
from core.models.teachers import Teacher
from core.models.students import Student
from sqlalchemy.types import Enum as BaseEnum
from sqlalchemy import or_


class GradeEnum(str, enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'


class AssignmentStateEnum(str, enum.Enum):
    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    GRADED = 'GRADED'


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, db.Sequence('assignments_id_seq'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable=False)
    content = db.Column(db.Text)
    grade = db.Column(BaseEnum(GradeEnum))
    state = db.Column(BaseEnum(AssignmentStateEnum), default=AssignmentStateEnum.DRAFT, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Assignment %r>' % self.id

    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)

    @classmethod
    def get_by_id(cls, _id):
        return cls.filter(cls.id == _id).first()

    @classmethod
    def upsert(cls, assignment_new: 'Assignment'):
        if assignment_new.id is not None:
            assignment = Assignment.get_by_id(assignment_new.id)
            assertions.assert_found(assignment, 'No assignment with this id was found')
            assertions.assert_valid(assignment.state == AssignmentStateEnum.DRAFT,
                                    'only assignment in draft state can be edited')

            assignment.content = assignment_new.content
        else:
            assignment = assignment_new
            db.session.add(assignment_new)

        db.session.flush()
        return assignment

    @classmethod
    def submit(cls, _id, teacher_id, auth_principal: AuthPrincipal):
        assignment = Assignment.get_by_id(_id)
        assertions.assert_found(assignment, 'No assignment with this id was found')
        if assignment.state != AssignmentStateEnum.DRAFT:
           assertions.assert_valid(False, 'only a draft assignment can be submitted')
        assertions.assert_valid(assignment.student_id == auth_principal.student_id, 'This assignment belongs to some other student')
        assertions.assert_valid(assignment.content is not None, 'assignment with empty content cannot be submitted')
        assertions.assert_valid(assignment.teacher_id == auth_principal.teacher_id, 'This assignment belongs to a different teacher')


        assignment.teacher_id = teacher_id
        assignment.state = AssignmentStateEnum.SUBMITTED
        db.session.flush()

        return assignment


    @classmethod
    def mark_grade(cls, _id, grade, auth_principal: AuthPrincipal):
        assignment = Assignment.get_by_id(_id)
        assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_valid(grade is not None, 'assignment with empty grade cannot be graded')
        assertions.assert_valid(assignment.state != AssignmentStateEnum.DRAFT, 'Draft assignments cannot be graded')
        if auth_principal.user_id != 5 and assignment.teacher_id != auth_principal.teacher_id:
            assertions.assert_valid(False, 'You cannot grade an assignment that is not yours')

        if assignment.state == AssignmentStateEnum.GRADED:
            if auth_principal.user_id != 5:  
                assertions.assert_valid(False, 'Only the principal can regrade this assignment')
        assignment.grade = grade
        assignment.state = AssignmentStateEnum.GRADED
        db.session.commit()
        return assignment

    @classmethod
    def get_assignments_by_student(cls, student_id):
        student = Assignment.get_by_id(student_id)  
        if not student:
            assertions.assert_found(False,"Student not found") 
        return cls.query.filter(cls.student_id == student_id).all()




    @classmethod
<<<<<<< HEAD
    def get_graded_and_submitted_assignments(cls):
        """Returns all assignments that are either graded or submitted."""
        return cls.filter(
            or_(cls.state == AssignmentStateEnum.GRADED, cls.state == AssignmentStateEnum.SUBMITTED)
        ).all()
    @classmethod
    def get_assignments_by_teacher(cls,teacher_id):
        """Return assignments based on the teacher ID."""
        teacher = Assignment.get_by_id(teacher_id)  
        if not teacher:
            abort(404, description="Teacher not found")
        return cls.query.filter(cls.teacher_id == teacher_id).all()

=======
    def get_assignments_by_teacher(cls):
        return cls.query.all()

    @classmethod
    def get_assignments_by_principal(cls):
        return cls.filter(cls.state != AssignmentStateEnum.DRAFT).all()
>>>>>>> upstream/main
