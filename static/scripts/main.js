function update(obj) {
    var id = obj.id;
    var url = "/update?id="+id;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.send();
    xhr.onreadystatechange = function() {
        location.reload();
    }
}

