function handleFiles(files) {
    for (let i = 0; i < fileListLength; i++) {
        output.innerText = `${output.innerText}\n${files.item(i).name}`;
    }
}

//async function AJAXSubmit(oFormElement) {
//    var resultElement = oFormElement.elements.namedItem("result");
//    const formData = new FormData(oFormElement);

//    try {
//        const response = await fetch(oFormElement.action, {
//            method: 'POST',
//            body: formData
//        });

//        if (response.ok) {
//            window.location.href = '/';
//        }

//        resultElement.value = 'Result: ' + response.status + ' ' +
//            response.statusText;
//    } catch (error) {
//        console.error('Error:', error);
//    }
//}

"use strict";

function AJAXSubmit(oFormElement) {
    var oReq = new XMLHttpRequest();
    oReq.onload = function (e) {
        oFormElement.elements.namedItem("result").value =
            'Result: ' + this.status + ' ' + this.statusText;
    };
    oReq.open("post", oFormElement.action);
    oReq.send(new FormData(oFormElement));
}