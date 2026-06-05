fetch("/customers")
.then(response => response.json())
.then(data => {

    let rows = "";

    data.forEach(customer => {

        rows += `
        <tr>
            <td>${customer[0]}</td>
            <td>${customer[1]}</td>
            <td>${customer[2]}</td>
            <td>${customer[3]}</td>
            <td>₹${customer[4]}</td>
            <td>${customer[6]}</td>
            <td>${customer[8]}</td>
            <td>${customer[9]}</td>
            <td>${customer[13]}</td>
            <td>₹${customer[14]}</td>
        </tr>
        `;
    });

    document.getElementById("customerTable").innerHTML = rows;

})
.catch(error => {
    console.log("Error:", error);
});