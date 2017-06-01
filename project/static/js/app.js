(function(){

google.load('visualization', '1', {packages: ['corechart']});

google.setOnLoadCallback(function() {        
        angular.bootstrap(document.body, ['WeatherAnalysis']);
    });

var app = angular.module('WeatherAnalysis',['ngRoute']);

app.config(function($routeProvider){
  $routeProvider  
  
  .when('/Regression',{
    templateUrl : '/static/Home.html',
    controller : 'RegressionDataController'
  })

  .when('/Clustering',{
    templateUrl : '/static/Temperature.html',
    controller : 'ClusterDataController'
  })

  .when('/Visualization',{
    templateUrl : '/static/visualization.html',
    controller : 'RegressionDataController'
  })
  
  .otherwise({redirectTo: '/'})
});

app.controller('ClusterDataController', function($scope, ClusterService , $timeout) {

  
  $scope.temp=[];
  $scope.Coord = [];
  $scope.Month=1
  $scope.Year=2010
  $scope.MonthList = { January: 1, Feb:2, March:3, April:4, May:5, June:6, July:7, August:8, September:9, October:10, November:11, December:12}
  $scope.ListOfCity = []
  $scope.ListOfCountry = []
  $scope.ListOfYear = []
  $scope.CoordPredictedTempClass=""
  $scope.Latitude = 100
  $scope.Longitude = 100

  $scope.map = new google.maps.Map(document.getElementById('map'), {
        zoom: 2,
        center: {lat: 37.090, lng: -95.712},
        mapTypeId: 'terrain'
      });

  


  $scope.$watch( ClusterService.ListOfCity, function () 
  {
    $scope.ListOfCity = ClusterService.ListOfCity();
  });

  $scope.$watch( ClusterService.ListOfCountry, function () 
  {
    $scope.ListOfCountry = ClusterService.ListOfCountry();
  });

  $scope.$watch( ClusterService.ListOfYear, function () 
  {
    $scope.ListOfYear = ClusterService.ListOfYear();
  });

  $scope.$watch( ClusterService.CoordPredictedTempClass, function () 
  {    
    $scope.CoordPredictedTempClass = ClusterService.CoordPredictedTempClass();
  });

  

  $scope.$watch( ClusterService.temp, function () 
  {    

    $scope.temp = ClusterService.temp();
    $scope.Coord = ClusterService.Coord();

    $scope.cityCircle = null
    
    for (var index = 0; index < $scope.Coord.length; index++) {
          var element = $scope.Coord[index];
          var t = $scope.temp[index]

          if ($scope.cityCircle != null)
            delete($scope.cityCircle)

          var color = '#FF0000' //Red
          if(t == 'Cold_Temperature')
          {
            color = '#9966FF' //Blue
          }
          else if(t == 'Medium_Temperature')
          {
            color = '#99FF00' //Yellow
          }

          $scope.cityCircle = new google.maps.Circle({
            strokeColor: color,
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: color,
            fillOpacity: 0.35,
            map: $scope.map,
            center: {lat: element[0], lng: element[1]},
            radius: 100000
          });

        }       

  });

  $scope.getListofCountryCity = function()
  {
      ClusterService.getListofCountryCity();
  }

  $scope.getCoordinateClusterData = function(){
    ClusterService.getCoordinateClusterData($scope.Year, $scope.Month)
  }

  $scope.getCoordinateTemperaturePrediction = function(){
    $scope.CoordPredictedTempClass=""
    ClusterService.getCoordinateTemperaturePrediction($scope.Year, $scope.Month, $scope.Longitude, $scope.Latitude)
  }
});


app.factory( 'ClusterService', function($http) { 

  var map
  var temp = []
  var Coord = []
  var ListOfCity = []
  var ListOfCountry = []
  var ListOfYear = []
  var CoordPredictedTempClass

  return {

      getListofCountryCity: function()
      {
        $http.get("http://127.0.0.1:5000/ListofCountryCity").then(function successCallback(response) 
          { 
            
            ListOfCity = response.data.city;
            ListOfCountry = response.data.country;
            ListOfYear = response.data.year;

            console.log(response);
            
            }, function successCallback(response) 
            {
              alert("Server has some problem. Please try after sometime.");
            })
      },

      getCoordinateClusterData: function(Year,Month)
        {
          $http({
              method  : 'POST',
              url     : 'http://127.0.0.1:5000/TemperatureClassificationForCoordinates',
              headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
              transformRequest: function(obj) {
                  var str = [];
                  for(var p in obj)
                  str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                  return str.join("&");
              },
              data: {"Month": Month, "Year" : Year}
          }).success(function(data) {                  
                  
                  Coord = data.coordinates;
                  temp = data.Temp_Class;		
                })
              .error(function(data) {
                    alert("Server has some problem. Please try after sometime.");
                });
        },

        getCoordinateTemperaturePrediction: function(Year,Month, Longitude, Latitude)
        {
          $http({
              method  : 'POST',
              url     : 'http://127.0.0.1:5000/TemperaturePredictionForCoordinates',
              headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
              transformRequest: function(obj) {
                  var str = [];
                  for(var p in obj)
                  str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                  return str.join("&");
              },
              data: {"Month": Month, "Year" : Year, "Longitude": Longitude, "Latitude":Latitude}
          }).success(function(data) {                  
                  
                  CoordPredictedTempClass = data.pred;
                })
              .error(function(data) {
                    alert("Server has some problem. Please try after sometime.");
                });
        },

         

        CoordPredictedTempClass:function()
        {
          return CoordPredictedTempClass;
        },

        temp:function()
        {
          return temp;
        },

        Coord:function()
        {
          return Coord;
        },

        ListOfCity:function()
        {
          return ListOfCity;
        },

        ListOfCountry:function()
        {
          return ListOfCountry;
        },

        ListOfYear:function()
        {
          return ListOfYear;
        },
                
      };
});

app.controller('RegressionDataController', function($scope, RegressionService , $timeout) {
      

      $scope.CityAvgTempData=[[1,2],[2,3],[3,4],[5,6],[7,8]] 
      $scope.PredictedTemp = "" 
      $scope.City = "Delhi"
      $scope.Country = "India"
      $scope.Month = 1
      $scope.Year = ""
      $scope.NumberOfYears = 100

      $scope.MonthList = { January: 1, Feb:2, March:3, April:4, May:5, June:6, July:7, August:8, September:9, October:10, November:11, December:12}
      $scope.ListOfCity = []
      $scope.ListOfCountry = []
      $scope.ListOfYear = []


      $scope.chart = new google.visualization.ScatterChart(document.getElementById('Regression'));     
      

      $scope.$watch( RegressionService.CityAvgTempData, function () 
      {
          $scope.CityAvgTempData = JSON.stringify(RegressionService.CityAvgTempData());        

          var data = new google.visualization.DataTable();
            data.addColumn('number', 'Year');
            data.addColumn('number', 'temp');
            data.addRows(JSON.parse($scope.CityAvgTempData));

          var options = {
            title: 'Year vs. Avg Temperature',
            hAxis: {title: 'Year'},
            vAxis: {title: 'Avg Temperature'},
            legend: 'none',
            trendlines: { 0: {} }
          };

          // Instantiate and draw our chart, passing in some options.
          
          $scope.chart.draw(data, options);

          $scope.Coefficient = RegressionService.Coefficient()
          $scope.Intercept = RegressionService.Intercept()

      }),
      
      $scope.$watch( RegressionService.PredictedTemp, function () 
      {
        $scope.PredictedTemp = RegressionService.PredictedTemp();
      });

      $scope.$watch( RegressionService.ListOfCity, function () 
      {
        $scope.ListOfCity = RegressionService.ListOfCity();
      });

      $scope.$watch( RegressionService.ListOfCountry, function () 
      {
        $scope.ListOfCountry = RegressionService.ListOfCountry();
      });

      $scope.$watch( RegressionService.ListOfYear, function () 
      {
        $scope.ListOfYear = RegressionService.ListOfYear();
      });
      

    $scope.getPredictedTemp = function()
    {      
      RegressionService.getPredictedTemp($scope.City, $scope.Country, $scope.Month, $scope.Year);
    } 

    $scope.getCityAvgTempData = function()
    {      
      console.log("Get city Avg Temp")
      RegressionService.getCityAvgTempData($scope.City, $scope.Country, $scope.Month, $scope.NumberOfYears);
    }

    $scope.getListofCountryCity = function()
    {
        RegressionService.getListofCountryCity();
    }

  });
  




  app.factory( 'RegressionService', function($http) { 

  var CityAvgTempData=[[1,2],[2,3],[3,4],[5,6],[7,8]]
  var PredictedTemp = ""
  var Coefficient = ""
  var Intercept = ""

  var ListOfCity = []
  var ListOfCountry = []
  var ListOfYear = []
  

  return {

      getListofCountryCity: function()
      {
        $http.get("http://127.0.0.1:5000/ListofCountryCity").then(function successCallback(response) 
          { 
            
            ListOfCity = response.data.city;
            ListOfCountry = response.data.country;
            ListOfYear = response.data.year;

            
            
            }, function successCallback(response) 
            {
              alert("Server has some problem. Please try after sometime.");
            })
      },

      getCityAvgTempData: function(City, Country, Month, NumberOfYears)
        {
          console.log("send details");
          $http({
              method  : 'POST',
              url     : 'http://127.0.0.1:5000/AvgMonthTemp',
              headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
              transformRequest: function(obj) {
                  var str = [];
                  for(var p in obj)
                  str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                  return str.join("&");
              },
              data: {"City": City, "Country" : Country, "Month":Month, "NumberOfYears":NumberOfYears}
          }).success(function(data) {
                  console.log(data);
                  CityAvgTempData = data.data;
                  Coefficient = data.cofficient;
                  Intercept = data.intercept;
                })
              .error(function(data) {
                    alert("Server has some problem. Please try after sometime.");
                });
        },

        ListOfCity:function()
        {
          return ListOfCity;
        },

        ListOfCountry:function()
        {
          return ListOfCountry;
        },

        ListOfYear:function()
        {
          return ListOfYear;
        },

        CityAvgTempData:function()
        {
          return CityAvgTempData;
        }, 

        Coefficient:function()
        {
          return Coefficient;
        },

        Intercept:function()
        {
          return Intercept;
        }, 


        getPredictedTemp: function(City, Country, Month, Year)
        {
          $http({
              method  : 'POST',
              url     : 'http://127.0.0.1:5000/AvgTempForSpecifiedMonthWithRegression',
              headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
              transformRequest: function(obj) {
                  var str = [];
                  for(var p in obj)
                  str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                  return str.join("&");
              },
              data: {"City": City, "Country" : Country, "Month":Month, "Year":Year}
          }).success(function(data) {
                  
                  PredictedTemp = data                  
                })
              .error(function(data) {
                    alert("Server has some problem. Please try after sometime.");
                });
        },

        PredictedTemp:function()
        {
          return PredictedTemp;
        },    
      };
});

})();