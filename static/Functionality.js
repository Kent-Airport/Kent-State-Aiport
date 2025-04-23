/*-------------Customer Support---------------*/


function scrollToSection(sectionId, offset = 350) {
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        const topPosition = targetSection.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: topPosition, behavior: 'smooth' });
    }
}

/*--------------Flights Page------------------*/


function AddFlight(Airline, Plane, DD, Dest){
    var table = document.getElementById("allFlightsTable");
    var flightEntry = table.insertRow();

    var airline = flightEntry.insertCell(0);
    var plane = flightEntry.insertCell(1);
    var dd = flightEntry.insertCell(2);
    var dest = flightEntry.insertCell(3);

    airline.textContent=Airline;
    plane.textContent=Plane;
    dd.textContent=DD;
    dest.textContent=Dest;
}
//12 entries of dummy data that would be replaced by reading the database and adding them with a foreach
AddFlight("Delta", "737", "05/12/25", "Cleveland");
AddFlight("American Airlines", "A320", "06/15/25", "New York");
AddFlight("United", "777", "07/20/25", "Chicago");
AddFlight("Southwest", "737", "08/10/25", "Dallas");
AddFlight("JetBlue", "A321", "09/05/25", "Boston");
AddFlight("Alaska Airlines", "737", "10/01/25", "Seattle");
AddFlight("Spirit Airlines", "A319", "11/14/25", "Miami");
AddFlight("Air Canada", "A330", "12/23/25", "Toronto");
AddFlight("Hawaiian Airlines", "A321", "01/05/26", "Honolulu");
AddFlight("Lufthansa", "A350", "02/16/26", "Frankfurt");
AddFlight("British Airways", "747", "03/12/26", "London");
AddFlight("Emirates", "A380", "04/18/26", "Dubai");
