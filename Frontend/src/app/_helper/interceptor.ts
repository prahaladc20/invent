import { Injectable, Injector } from '@angular/core';
import {HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';
// import 'rxjs/add/observable/throw'
// import 'rxjs/add/operator/catch';
// @Injectable()
export class Interceptor implements HttpInterceptor {
    constructor() {}
    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        
        let currentUser = JSON.parse(localStorage.getItem('currentUser'));
        if (currentUser && currentUser['access']) {
            request = request.clone({
                setHeaders: { 
                    Authorization: `Bearer ${currentUser['access']}`
                }
            });
        }

        return next.handle(request);
    }
    
}