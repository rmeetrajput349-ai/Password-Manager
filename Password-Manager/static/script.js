function togglePassword(id) {
    let field = document.getElementById(id);
    if (field.type === "password") {
        field.type = "text";
    } else {
        field.type = "password";
    }
}

function copyPassword(id) {
    let field = document.getElementById(id);
    field.select();
    navigator.clipboard.writeText(field.value);
    alert("Copied!");
}