import { Injectable } from '@angular/core';
import { HttpHeaders,HttpErrorResponse, HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class AccountService {
  
  login_url = 'http://127.0.0.1:8000/api/login/';
  // private options = { headers: new HttpHeaders().set('Content-Type', 'application/json') };


  constructor(private http: HttpClient) { }
  authenticate(username: string, password: string) {
    return this.http.post<any>(this.login_url, { username, password })
        .pipe(map(user => {
          console.log(user, "check user")
            // login successful if there's a jwt token in the response
            if (user && user['access']) {
                // store user details and jwt token in local storage to keep user logged in between page refreshes
                localStorage.setItem('currentUser', JSON.stringify(user));
                localStorage.setItem('Role',user['groups'][0]);
            }

            return user;
        }));
}


  logout() {
    // remove user from local storage to log user out
    // alert("ll")
    // localStorage.removeItem('currentUser');
    localStorage.clear();
    sessionStorage.clear();
}
}
