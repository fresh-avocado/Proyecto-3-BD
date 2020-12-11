export default {
     computed: {
          filterTweets() {
               console.log("Filter tweets");
               return this.tweets.filter( (tweet) => {
                    if (tweet.text) {
                         console.log("tweet.text:");
                         console.log(tweet.text);
                         let matched = tweet.text.toLowerCase().match(this.filterResult.toLowerCase());
                         console.log(`matched: ${matched}`);
                         return matched;
                    } else {
                         return false;
                    }
               });
          },
     }
}