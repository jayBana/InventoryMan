// main app module and with injected components
var myApp = angular.module('myApp', ['ngRoute', 'ui.bootstrap', 'ngAnimate', 'ngTable', 'ngResource']);

myApp.config(['$routeProvider', function ($routeProvider) {
    // set up routing
    $routeProvider.
        when('/', {
            title: 'Orders',
            templateUrl: '../static/partials/ordersList.html',
            controller: 'OrdersListCtrl'
        }).
        otherwise({
            redirectTo: '/'
        }).
        when('/info', {
            title: 'Information',
            templateUrl: '../static/partials/infoList.html',
            controller: 'InfoListCtrl'
        });
}]);