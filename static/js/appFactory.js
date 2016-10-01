app.factory('appFactory', ['$http', function($http){
	return {
		var saveCredentials = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/saveCredentials', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getAllReports = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getAllReports', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getTotalMessageReport = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getTotalMessageReport', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getSwearWordReport = funtion (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getSwearWordReport', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getMostLikedReport = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getMostLikedReport', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getBiggestLikerReport = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getBiggestLikerReport', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getMemeLordReport = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getMemeLordReport', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getDonaldTrumpReport = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getDonaldTrumpReport', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getDudeReport = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getDudeReport', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getGFBFReport = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getGFBFReport', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getSingleWordReport = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getSingleWordReport', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getMostPopularHourReport = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getMostPopularHourReport', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getMostPopularDayReport = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getMostPopularDayReport', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getMostPopularWeekReport = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getMostPopularWeekReport', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getMultipleWordReport = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getMultipleWordReport', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getPhraseReport = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getPhraseReport', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		},

		var getOutputReport = function (credentials){
			var report = {}
			var parameters = credentials;
			$http.get('api/getOutputReport', { params: parameters })
				.success(function(data){
					angular.copy(data, report)
			})
			return report;
		}
	}
}]);