function showLoaderOnClick(url,index_url,confirmation = true) {
      if (confirmation){
      window.location=url;
      } else {
           return false;
       }
      $(window).on('load', function () {
      window.location=index_url;
      })
  }

