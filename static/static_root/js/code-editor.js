/**
 * Created by user on 05/10/2015.
 */

var editor = ace.edit("inner-editor");
editor.setTheme("ace/theme/monokai");
editor.getSession().setMode("ace/mode/c_cpp");
editor.setValue("#include<stdio.h>\n#include<stdlib.h>\nint main()\n{\n}");

$("#java").click(function () {

    var editor = ace.edit("inner-editor");
    editor.getSession().setMode("ace/mode/java");
    editor.setValue("import java.io.*;\nimport java.util.*;\nclass Solution{\n}");
    $("#lang_choose").text("Java");
});
$("#python").click(function () {
    var editor = ace.edit("inner-editor");
    editor.getSession().setMode("ace/mode/python");
    editor.setValue("print 'hello world'");
    $("#lang_choose").text("Python");
});
$("#c").click(function () {
    var editor = ace.edit("inner-editor");
    editor.getSession().setMode("ace/mode/c_cpp");
    editor.setValue("#include<stdio.h>\n#include<stdlib.h>\nint main()\n{\n}");
    $("#lang_choose").text("C");
});
$("#cpp").click(function () {
    var editor = ace.edit("inner-editor");
    editor.getSession().setMode("ace/mode/c_cpp");
    editor.setValue("#include<iostream>\nusing namespace std;\nint main()\n{\n}");
    $("#lang_choose").text("CPP");
});

