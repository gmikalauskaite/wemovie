<template>
<div class="container">
    <div class="row">
        <div class="col-2">
        </div>
        <div class="col-8">
            <label for="roomtext" class="form-label">Room Name</label>
            <input type="text" v-model="roomName" id="roomtext" class="form-control">
            <button @click="enterRoom" class="btn btn-primary">Join</button>
            <button @click="createRoom" class="btn btn-secondary">Create</button>

              <div v-if="joinedRoomName">
              <h1 id="roomHeader">{{ joinedRoomName }}'s movie room </h1>
              <div class="card" v-for="(k, v) in movies">
                  <div class="row g-0">
                      <div class="col-4">
                          <img :src="k.cover" class="img-fluid rounded-start">
                      </div>
                      <div class="col-8">
                          <div class="card-body">
                              <h1 class="card-title">{{ v }} ({{ k.release }})</h1>
                              <h5 class="card-subtitle"> ★ {{ k.rating }}/10</h5>
                              <p class="card-text">
                                  {{ k.description }}
                              </p>
                              <button 
                                class="btn btn-success"
                                @click="vote(v)"
                                :disabled="hasVoted(v)"
                                >Vote ({{k.votes}})
                              </button>

                              <button
                              class="btn btn-danger"
                              @click="removeMovie(v)"
                              >
                              Delete
                              </button>
                          </div>
                      </div>
                  </div>
              </div>
            </div>

            <h1>Search</h1>

            <label for="searchText" class="form-label">Movie Name</label>
            <input type="text"
            v-model="searchString"
            class="form-control"
            id="searchText"
            placeholder="John Wick">
            <button @click="search" class="btn btn-primary">Search</button>

            <div class="card" v-for="suggest in suggestions">
                <div class="row g-0">
                    <div class="col-4">
                        <img :src="suggest.cover" class="img-fluid rounded-start">
                    </div>
                    <div class="col-8">
                        <div class="card-body">
                            <h1 class="card-title">{{ suggest.title}} ({{ suggest.release }})</h1>
                            <h5 class="card-subtitle"> ★ {{ suggest.rating }}/10</h5>
                            <p class="card-text">
                                {{ suggest.description }}
                            </p>
                            <button class="btn btn-primary" @click="addMovie(suggest)">Add</button>
                        </div>
                    </div>
                </div>
            </div>
            <hr>
        </div>
    </div>
</div>
</template>

<style>
div .card {
  margin: 20px;
  border-radius: 2%;
}

#roomHeader {
  text-align: center;
}

</style>

<script>
import axios from 'axios';

export default {
  data: function() {
    return {
      movieTitle: "",
      roomName: "",
      joinedRoomName: "",
      votes: {},
      voted: false,
      searchString: "",
      movies: {},
      suggestions: []
    }
  },
  mounted: function() {
    var root = this;
    if (root.roomName == "") {
      return;
    }
  },
  methods: {
    hasVoted: function(title) {
      return this.votes[title] == true;
    },
    enterRoom: function() {
      var root = this;
      axios.get('http://localhost:3000/movies', {
        params: {
          room_name: root.roomName
        }
      }).then(function (resp) {
        root.movies = resp.data;
        root.joinedRoomName = root.roomName;
        root.votes = {}
      });
    },
    createRoom: function() {
      var root = this;
      axios.post('http://localhost:3000/room', {
        name: this.roomName
       }).then(function (resp) {
        root.movies = [];
        root.joinedRoomName = root.roomName;
        root.votes = {}
       });
    },
    search: function() {
      var root = this;
      console.log(root.searchString);
      axios.get('http://localhost:3000/search', {
        params: {
          title: root.searchString
        }
      }).then(function(resp) {
        root.suggestions = resp.data;
      });
    },
    addMovie: function(movie) {
      var root = this;
      axios.post('http://localhost:3000/movies', movie, {
        params: {
          room_name: root.roomName
        }
      }).then(function (resp) {
        console.log(resp.data);
        root.movies = resp.data;
      });
    },
    removeMovie: function(title) {
      var root = this;
      axios.delete('http://localhost:3000/movies', { 
        params: {
          title: title,
          room_name: root.roomName
        }
      }).then(function (resp) {
        root.movies = resp.data; 
      });
    },
    vote: function(data) {
      this.voted = true;
      this.votes[data] = true;

      var root = this;
      axios.post('http://localhost:3000/vote', null, { 
        params: {
          title: data,
          room_name: root.roomName
        }
      }).then(function (resp) {
        root.movies = resp.data; 
      });
    }
  }
}
</script>

