myApp.controller('OrdersListCtrl', ['$scope', 'Data', 'ngTableParams', function ($scope, Data, ngTableParams) {
    var tomorrow = moment().add(1, 'd');
    $scope.start_date = tomorrow.format("YYYY-MM-DD");
    $scope.end_date = tomorrow.add(6, 'd').format("YYYY-MM-DD");

    // get the data from the server
    Data.get("data").then(function (data) {
        $scope.data = data.orders;
        $scope.tableParams = new ngTableParams({
            page: 1,            // show first page
            count: 500          // count per page
        }, {
            groupBy: 'name',
            total: $scope.data.length,
            counts: [], // disable paging
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
