myApp.controller('InfoListCtrl', ['$scope', 'Data', function ($scope, Data) {
    // get data from server for weather
    Data.get('weather').then(function (data) {
        $scope.weather = data.weather;
    });

    // setup table headers for weather
    $scope.w_headers = [
        {text: "Icon"},
        {text: "Date"},
        {text: "Day"},
        {text: "Description"},
        {text: "Temperature (°C)"},
        {text: "Precipitation (mm)"},
        {text: "Wind (km/h)"},
        {text: "Cloud Cover (%)"}
    ]

    // get data from server for events
    Data.get('events').then(function (data) {
        $scope.events = data.events;
    });

    // set up headers for events
    $scope.e_headers = [
        {text: "Start"},
        {text: "Day"},
        {text: "End"},
        {text: "Venue"},
        {text: "Title"}
    ]

    // get the day name
    $scope.getDay = function (date) {
        return moment(date).get().format('dddd');
    }

    // get start date by splitting string and removing hr:min:sec
    $scope.getStartDate = function (date) {
        if (date === null) {
            return;
        }
        var d = date.split(" ");
        return d[0];
    }

    // get end date by splitting string and removing hr:min:sec
    // we only want end dates for events that are on for more than one day
    $scope.getEndDate = function (sdate, edate) {
        if (edate === null || sdate.substring(0, 10) === edate.substring(0, 10)) {
            return
        }
        var d = edate.split(" ");

        return d[0];
    }

    // get the time when the event starts
    // if it is "00:00:00" then just discard it
    $scope.getTime = function (date) {
        var d = date.split(" ");
        if (d[1] === "00:00:00") {
            return "";
        } else {
            return d[1].substring(0, 5);
        }
    }
}]);
