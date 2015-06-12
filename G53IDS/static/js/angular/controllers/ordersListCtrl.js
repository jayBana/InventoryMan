myApp.controller('OrdersListCtrl', ['$scope', 'Data', 'ngTableParams', function ($scope, Data, ngTableParams) {
    var tomorrow = moment().add(1, 'd');
    $scope.start_date = tomorrow.format("YYYY-MM-DD");
    $scope.end_date = tomorrow.add(6, 'd').format("YYYY-MM-DD");

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


    $scope.calcSum = function (data) {
        var sum = 0;
        angular.forEach(data, function (item) {
            sum += item.quantity;
        });
        return Math.ceil(sum).toLocaleString();
    }
}]).controller('groupCtrl', function($scope) {
    $scope.group.$hideRows = true;
});
