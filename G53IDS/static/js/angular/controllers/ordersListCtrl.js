myApp.controller('OrdersListCtrl', ['$scope', 'Data', 'ngTableParams', function ($scope, Data, ngTableParams) {
    // set up date related variables in scope
    // upon login show a 7 days of prediction as from tomorrow
    var tomorrow = moment().add(1, 'd');
    $scope.start_date = tomorrow.format("YYYY-MM-DD");
    $scope.end_date = tomorrow.add(6, 'd').format("YYYY-MM-DD");

    // get the data from the server
    Data.get("data").then(function (data) {
        $scope.data = data.orders;
        // this goes here, so that the table is only loaded when
        // that AJAX call for getting data has been successful
        $scope.tableParams = new ngTableParams({
            page: 1,            // show first page
            count: 500          // count per page
        }, {
            groupBy: 'name', // use order item name for grouping
            total: $scope.data.length,
            counts: [], // disable paging
            // delayed getting of data
            getData: function ($defer, params) {
                $defer.resolve($scope.data);
            }
        });
    });

    // get the day name
    $scope.getDay = function (date) {
        return moment(date).get().format('dddd');
    }

    // calculate the sum of each item dynamically
    $scope.calcSum = function (data) {
        var sum = 0;
        angular.forEach(data, function (item) {
            sum += item.quantity;
        });
        return Math.ceil(sum).toLocaleString();
    }


    // prevents the expansion of groups on startup
}]).controller('groupCtrl', function ($scope) {
    $scope.group.$hideRows = true;
});
