import { Component, OnInit } from '@angular/core';
import { AccountService } from '../_service/account.service';
import { Router, ActivatedRoute } from '@angular/router';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-account',
  templateUrl: './account.component.html',
  styleUrls: ['./account.component.css'],
  providers:[AccountService]
})
export class AccountComponent implements OnInit {
  loginForm: FormGroup;
  loading = false;
  submitted = false;
  returnUrl: string;
  error = '';

  constructor( 
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private accountService: AccountService) { }

    _
    ngOnInit() {
      this.loginForm = this.formBuilder.group({
        username: ['', Validators.required],
        password: ['', Validators.required]
      });

      this.accountService.logout();
  
      this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
    }

    get f() {
      return this.loginForm.controls;
    }

    onSubmit() {
      this.submitted = true;

      // stop here if form is invalid
      if (this.loginForm.invalid) {
          return;
      }

      this.loading = true;
      this.accountService.authenticate(this.f.username.value, this.f.password.value)
          .pipe(first())
          .subscribe(
              data => {
                console.log(this.f.username.value,'data')
                sessionStorage.setItem('loggedUser', this.f.username.value);
                  this.router.navigate(['inventory']);
              },
              error => {
                  this.error = error;
                  this.loading = false;
              });
  }
   

}