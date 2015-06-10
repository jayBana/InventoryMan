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

}]);