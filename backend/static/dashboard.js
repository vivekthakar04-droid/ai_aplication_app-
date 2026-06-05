// Dashboard Data Load

fetch("/dashboard")
  .then(response => response.json())
  .then(data => {

    document.getElementById("total").innerText =
      data.total_customers;

    document.getElementById("paid").innerText =
      data.paid;

    document.getElementById("overdue").innerText =
      data.overdue;

    document.getElementById("outstanding").innerText =
      "₹" + Number(data.outstanding_balance).toLocaleString();

  })
  .catch(error => {
    console.log("Error:", error);
  });


// Pie Chart

new Chart(
  document.getElementById("pieChart"),
  {
    type: "pie",
    data: {
      labels: ["Paid", "Unpaid", "Overdue"],
      datasets: [{
        data: [65, 20, 15]
      }]
    }
  }
);


// Line Chart

new Chart(
  document.getElementById("lineChart"),
  {
    type: "line",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
      datasets: [{
        label: "Outstanding",
        data: [12000, 18000, 15000, 22000, 17000, 25000],
        fill: false
      }]
    }
  }
);


// Summary Chart

new Chart(
  document.getElementById("summaryChart"),
  {
    type: "doughnut",
    data: {
      labels: ["Email", "SMS", "WhatsApp"],
      datasets: [{
        data: [50, 25, 25]
      }]
    }
  }
);