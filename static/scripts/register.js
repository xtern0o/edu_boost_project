var teacher_button = document.getElementById('teacher-button');
var student_button = document.getElementById('student-button');
var enter_code_pole = document.getElementById('enter-code');

function switchRadioChoiceToTeacher() {
    teacher_button.checked = true;
    student_button.checked = false;
    enter_code_pole.hidden = true;
};

function switchRadioChoiceToStudent() {
    teacher_button.checked = false;
    student_button.checked = true;
    enter_code_pole.hidden = false;
};
