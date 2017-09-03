function mgw_toggle(source) {
    checkboxes = document.getElementsByName('MGW');
    for(var i=0, n=checkboxes.length;i<n;i++) {
        checkboxes[i].checked = source.checked;
    }
}


function source_operator_toggle(source) {
    checkboxes = document.getElementsByName('source_operator');
    for(var i=0, n=checkboxes.length;i<n;i++) {
        checkboxes[i].checked = source.checked;
    }
}


function destination_operator_toggle(source) {
    checkboxes = document.getElementsByName('destination_operator');
    for(var i=0, n=checkboxes.length;i<n;i++) {
        checkboxes[i].checked = source.checked;
    }
}

function operator_toggle(source) {
    checkboxes = document.getElementsByName('operator');
    for(var i=0, n=checkboxes.length;i<n;i++) {
        checkboxes[i].checked = source.checked;
    }
}
