var answerNum = 1;
function addAnswerFunc() {
    var newDiv = document.getElementById("node" + answerNum).cloneNode(true);
    answerNum += 1;
    newDiv.setAttribute("id", "node" + answerNum);
    newDiv.children[0].setAttribute("name", "answer" + answerNum);
    newDiv.children[0].setAttribute("id", "answerInput" + answerNum);
    newDiv.children[1].setAttribute("value", "");
    newDiv.children[1].setAttribute("name", "date" + answerNum);
    newDiv.children[1].setAttribute("value", "");
    newDiv.children[1].setAttribute("id", "answerDate" + answerNum);
    newDiv.children[2].setAttribute("name", "type" + answerNum);
    newDiv.children[2].setAttribute("id", "answerType" + answerNum);
    document.getElementById("QAFo").appendChild(newDiv);
}
function removeAnswerFunc() {
    var r = confirm("是否要删除最后一个答案？");
    if (r === true) {
        if (answerNum > 1) {
            var lastDiv = document.getElementById("node" + answerNum);
            document.getElementById("QAForm").removeChild(lastDiv);
            answerNum -= 1;
        } else {
            alert("至少要有一个答案")
        }
    }
}
function submitFunc() {
    var question = document.getElementById("question").value;
    //依次作检查
    if (question === "") {
        alert("当前问题为空！")
    }
    var isAllSameType = false;
    var isError = false;
    var preType = false;
    for (var i = 1; i <= answerNum; i++) {
        var div = document.getElementById("node" + i);
        var answer = div.children[0].value;
        var type = div.children[2].value;
        if (answer === "") {
            alert("某个答案为空！请检查");
            isError = true;
            break;
        }
        if (preType !== type && answerNum > 1) {
            isAllSameType = true;
        }
    }
    if (!isError) {
        if (isAllSameType) {
            r = confirm("当前问题均为同一类型, 是否确认提交？")
            if (!r) {
                return;
            }
        }
        for (var i = 1; i <= answerNum; i++) {
            var div = document.getElementById("node" + i);
            var answer = div.children[0].value;
            var date = div.children[1].value;
            var type = div.children[2].value;
            // 条件判断

            // 提交数据
            $.post("/example", {
                'question': question,
                'answer': answer,
                'date': date,
                'type': type
            }, function (data) {
                if (data['success']) {
                    alert(`提交成功`)
                } else {
                    alert(`提交失败`)
                }
            });
        }
    }
}
