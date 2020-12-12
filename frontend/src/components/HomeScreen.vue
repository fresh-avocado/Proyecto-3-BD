<template>
  <div id="container">
       <div id="inputs" class="super-item">
          <div id="query-section" class="item">
               <h2>Query</h2>
               <input type="file" accept=".jpg" v-on:change="prepareToQueryImage($event.target.name, $event.target.files)">
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
          <div id="file-section" class="item">
               <h2>Archivo para Indexar</h2>
               <input type="file" accept=".jpg" multiple name="file" v-on:change="prepareToUploadFile($event.target.name, $event.target.files)">
               <button v-on:click="uploadImages()">Indexar Archivo</button>
               <div v-if="processingFile">
                    <h3>Indexing file...</h3>
               </div>
          </div>
       </div>
       <div id="query-results" class="super-item" v-for="image in images" v-bind:key="image.id">
            <div class="image-container">
               <!-- TODO: adaptar para mostrar las imagenes bien bonito -->
               <h2>{{ image.name }}</h2>
            </div>
       </div>
  </div>
</template>

<script>

import axios from 'axios';

export default {
     name: 'HomeScreen',
     data() {
          return {
               selectedFiles: [],
               selectedImageQueryName: '',
               selectedImageQuery: '',
               processingQuery: false,
               processingFile: false,
               images: [],
               queryTime: '',
               queryWasProcessed: false,
               k: '',
          }
     },
     created() {
          console.log("component was created");
     },
     methods: {
          uploadImages() {
               if (this.selectedFiles.length === 0) {
                    alert("Seleccione un archivo para indexar.")
                    return;
               }
               console.log(`FILES: ${this.selectedFiles}`);
               this.processingFile = true;

               let formData = new FormData();

               formData.append('file', this.selectedFiles);

               axios.post(
                    'http://127.0.0.1:5000/uploadImages',
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
          prepareToQueryImage(name, files) {
               if (files.length === 0) {
                    console.log("Need one file to index.");
                    return;
               }
               console.log("Selected Query Name: " + this.selectedImageQueryName);
               this.selectedImageQueryName = name;
               this.selectedImageQuery = files[0];
          },
          prepareToUploadFile(name, files) {
               if (files.length === 0) {
                    console.log("Need one file to index.");
                    return;
               }
               this.selectedFiles = files;
          },
          processQuery() {
               // FIXME: arreglar validación
               // if (this.selectedImageQueryName === '') {
               //      alert("Debe seleccionar una imagen como query.")
               //      console.log("Cannot process empty query.");
               //      return;
               // }

               this.processingQuery = true;

               let formData = new FormData();

               formData.append('image', this.selectedImageQuery);

               axios.get(
                    `http://127.0.0.1:5000/queryImages?k=${this.k === '' ? -1 : this.k}`,
                    formData,
                    {
                         headers: {
                              'Content-Type': 'multipart/form-data',
                              'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',
                         }
                    }
               ).then( (response) => {
                    console.log("QUERY IMAGES RESPONSE:");
                    console.log(response);
                    if (typeof response.data !== 'undefined') {
                         this.queryTime = response.data.execTime;
                         this.images = response.data.images;
                         console.log("RETRIEVED IMAGES:");
                         console.log(this.images);
                    }
                    this.selectedImageQuery = '';
                    this.selectedImageQueryName = '';
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