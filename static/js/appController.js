app.controller('appController', ['$scope', 'appFactory', function($scope, appFactory){
	$scope.credentials = {
		access_token: '',
		nickname: '',
		display_name: '',
		group_name: ''
	}

	$scope.saveCredentials = function(credentials){
		appFactory.saveCredentials(credentials)
			.then(function(data){
				$scope.credentials = data;
			});
	}

	$scope.getAllReports = function(credentials){
		appFactory.getAllReports(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}

	$scope.getTotalMessageReport = function(credentials){
		appFactory.getTotalMessageReport(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}

	$scope.getSwearWordReport = function(credentials){
		appFactory.getSwearWordReport(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}

	$scope.getMostLikedReport = function(credentials){
		appFactory.getMostLikedReport(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}

	$scope.getBiggestLikerReport = function(credentials){
		appFactory.getBiggestLikerReport(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}

	$scope.getMemeLordReport = function(credentials){
		appFactory.getMemeLordReport(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}

	$scope.getDonaldTrumpReport = function(credentials){
		appFactory.getDonaldTrumpReport(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}

	$scope.getDudeReport = function(credentials){
		appFactory.getDudeReport(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}

	$scope.getGFBFReport = function(credentials){
		appFactory.getGFBFReport(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}

	$scope.getSingleWordReport = function(credentials){
		appFactory.getSingleWordReport(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}

	$scope.getMostPopularHourReport = function(credentials){
		appFactory.getMostPopularHourReport(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}

	$scope.getMostPopularDayReport = function(credentials){
		appFactory.getMostPopularDayReport(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}

	$scope.getMostPopularWeekReport = function(credentials){
		appFactory.getMostPopularWeekReport(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}

	$scope.getMultipleWordReport = function(credentials){
		appFactory.getMultipleWordReport(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}

	$scope.getPhraseReport = function(credentials){
		appFactory.getPhraseReport(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}

	$scope.getOutputReport = function(credentials){
		appFactory.getOutputReport(credentials)
			.then(function(data){
				$scope.report = data;
			});
	}
}]);