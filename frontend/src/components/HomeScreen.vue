<template>
  <div id="container">
       <div id="inputs" class="super-item">
          <div id="query-section" class="item">
               <h2>Query</h2>
               <input class="query-input" type="text" v-model="query" placeholder="Query...">
               <div class="space"></div>
               <input class="query-input" type="text" v-model="k" placeholder="k más relevantes (opcional)...">
               <div class="space"></div>
               <button v-on:click="processQuery()">Buscar</button>
               <div v-if="processingQuery">
                    <h3>Processing Query...</h3>
               </div>
               <div v-if="queryWasProcessed">
                    <h3>Query execution time: {{ queryTime }} ms.</h3>
               </div>
          </div>
          <div lass="item">
               <h2>Filter Resultados del Query</h2>
               <input type="text" v-model="filterResult" placeholder="Filtrar tweets...">
          </div>
          <div id="file-section" class="item">
               <h2>Archivo para Indexar</h2>
               <input type="file" name="file" v-on:change="prepareToUploadFile($event.target.name, $event.target.files)">
               <button v-on:click="uploadFile()">Indexar Archivo</button>
               <div v-if="processingFile">
                    <h3>Indexing file...</h3>
               </div>
          </div>
       </div>
       <div id="query-results" class="super-item" v-for="tweet in filterTweets" v-bind:key="tweet.id">
            <div class="tweet-container">
                 <p><strong>ID:</strong> {{ tweet.id }}</p>
                 <p><strong>Date:</strong> {{ tweet.date.substr(0, 19) }}</p>
                 <p><strong>Text:</strong> {{ tweet.text }}</p>
                 <p><strong>User ID:</strong> {{ tweet.user_id }}</p>
                 <p><strong>Username:</strong> {{ tweet.user_name }}</p>
                 <div v-if="tweet.retweeted">
                      <p><strong>Retweet Text:</strong> {{ tweet.RT_text }}</p>
                      <p><strong>Retweet User ID:</strong> {{ tweet.RT_user_id }}</p>
                      <p><strong>Retweet Username:</strong> {{ tweet.RT_user_name }}</p>
                 </div>
            </div>
       </div>
  </div>
</template>

<script>

import axios from 'axios';
import filterTweetsMixin from '../mixins/filterTweetsMixin';

export default {
     name: 'HomeScreen',
     data() {
          return {
               query: '',
               archivo: null,
               selectedName: '',
               selectedFiles: [],
               filterResult: '',
               processingQuery: false,
               processingFile: false,
               tweets: [],
               queryTime: '',
               queryWasProcessed: false,
               k: '',
          }
     },
     created() {
          console.log("component was created");
     },
     mixins: [
          filterTweetsMixin
     ],
     methods: {
          uploadFile() {
               if (this.selectedFiles.length === 0) {
                    alert("Seleccione un archivo para indexar.")
                    return;
               }
               console.log(`NAME: ${this.selectedName}`);
               console.log(`FILES: ${this.selectedFiles[0]}`);
               this.processingFile = true;

               let formData = new FormData();

               formData.append('file', this.selectedFiles[0]);

               axios.post(
                    'http://127.0.0.1:5000/uploadFile',
                    formData,
                    {
                         headers: {
                              'Content-Type': 'multipart/form-data',
                              'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',
                         }
                    }
               ).then((response) => {
                    console.log("UPLOAD FILE RESPONSE: " + response);
                    this.processingFile = false;
               }).catch(() => {
                    console.log("error occurred when uploading a file");
                    this.processingFile = false;
               });

          },
          prepareToUploadFile(name, files) {
               if (files.length === 0) {
                    console.log("Need one file to index.");
                    return;
               }
               this.selectedName = name;
               this.selectedFiles = files;
          },
          processQuery() {
               if (this.query === '') {
                    alert("El query debe tener al menos un caracter.")
                    console.log("Cannot process empty query.");
                    return;
               }

               this.processingQuery = true;

               axios.get(
                    `http://127.0.0.1:5000/queryTweets?query=${this.query}&k=${this.k === '' ? -1 : this.k}`,
                    {
                         headers: {
                              'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',
                         }
                    }
               ).then( (response) => {
                    console.log("QUERY TWEETS RESPONSE:");
                    console.log(response);
                    if (typeof response.data !== 'undefined') {
                         this.queryTime = response.data.execTime;
                         this.tweets = response.data.tweets;
                         console.log("RETRIEVED TWEETS:");
                         console.log(this.tweets);
                    }
                    this.query = '';
                    this.k = '';
                    this.queryWasProcessed = true;
                    this.processingQuery = false;
               }).catch(() => {
                    console.log("error occurred when processing query");
               });
          },
     },
}
</script>

<style>
     #inputs {
          display: flex;
          justify-content: space-evenly;
     }

     .query-input {
          width: 120%;
     }

     .space {
          width: 10%;
     }

     #query-results {
          display: flex;
          flex-direction: column;
          margin: 1%;
     }

     .tweet-container {
          flex-basis: 50%;
          border-color: black;
          border-style: solid;
     }
</style>