myApp.controller('OrdersListCtrl', ['$scope', 'Data', function ($scope, Data) {
    $scope.item = {};
    Data.get().then(function(data){
       $scope.items = data.orders;
    });
    $scope.columns = [
        {text:"Date"},
        {text:"Name"},
        {text:"Quantity"}
    ];
    var tomorrow = moment().add(1,'d');
    $scope.start_date = tomorrow.format("YYYY-MM-DD");
    $scope.end_date = tomorrow.add(6, 'd').format("YYYY-MM-DD");
}]);