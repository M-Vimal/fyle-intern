<<<<<<< HEAD
from flask import Blueprint, request
from marshmallow import ValidationError
from core import db
from core.libs import helpers, assertions

from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum,Teacher
from sqlalchemy.types import Enum as BaseEnum
from ..decorators import accept_payload, authenticate_principal
from .schema import AssignmentSchema, AssignmentGradeSchema,TeacherSchema
=======
from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema
>>>>>>> upstream/main
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
<<<<<<< HEAD
    all_assignments = Assignment.get_graded_and_submitted_assignments()
    all_assignments_dump = AssignmentSchema().dump(all_assignments, many=True)
    return APIResponse.respond(data=all_assignments_dump)

@principal_assignments_resources.route('/teacher', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    teachers = Teacher.get_teacher()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'],strict_slashes=False)
=======
    principals_assignments = Assignment.get_assignments_by_principal()
    principals_assignments_dump = AssignmentSchema().dump(principals_assignments, many=True)
    return APIResponse.respond(data=principals_assignments_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
>>>>>>> upstream/main
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
<<<<<<< HEAD
    print(incoming_payload)
    print(p)
        # Retrieve the assignment by its ID

    # Check if the assignment exists
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    # Proceed to mark the grade
=======
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
>>>>>>> upstream/main

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
<<<<<<< HEAD
    print(graded_assignment)

    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)


   
=======
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
>>>>>>> upstream/main
