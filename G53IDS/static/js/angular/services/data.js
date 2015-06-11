myApp.factory("Data", ['$http', '$location',
    function($http) {
        var obj = {};
        obj.get = function() {
            return $http.get('/data').then(function (results){
               return results.data;
            });
        };
        return obj;
}]);