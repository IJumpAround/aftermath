
let regex = RegExp(/\(.*X.*\)/);
function x_value_disabler(event) {

    let template = document.getElementById('id_template')
    let x_val = document.getElementById('id_x_value')
    let template_text = template.options[template.selectedIndex].text
    let x_value_value = x_val.value
    if(template.selectedIndex >= 0 && template.options[template.selectedIndex].text.search(regex) !== -1) {
        x_val.disabled = false
        console.log('enabled')
    } else if(template.selectedIndex >= 0 && x_val.disabled === false) {
        console.log('disabled')
        x_val.disabled = true;
        x_val.value = "";
    }
}


function x_value_valid(template_text, x_value_value) {
    console.log(template_text)
    console.log(x_value_value)
    if (template_text.search(regex) > 0) {
        return !(x_value_value.trim() === "");
    } else {
        return x_value_value === "";
    }
}
function form_validator(event) {
    let template = document.getElementById('id_template')
    let x_val = document.getElementById('id_x_value')
    let template_text = template.options[template.selectedIndex].text
    let x_value_value = x_val.value

    let result = x_value_valid(template_text, x_value_value)
    if (result === false) {
        console.log('invalid')
        alert("X value must be provided for a scaling trait and should not be provided with non-scaling traits.")
        event.preventDefault()
    }
}

window.onload = function() {
    let form = document.getElementById('weapontrait_form') ? document.getElementById('weapontrait_form') : document.getElementById('armortrait_form')
    let x_val = document.getElementById('id_x_value')
    if(form) {
        form.addEventListener("change", x_value_disabler, true);
        form.addEventListener("submit", form_validator, true);
        x_value_disabler()
    }
}
