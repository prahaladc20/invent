import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {InventryListComponent} from './inventry-list/inventry-list.component';
import {AccountComponent} from './account/account.component';

import {AuthGuardService as AuthGuard} from './auth/auth-guard.service';
import {InventoryComponent} from "./inventory/inventory.component";

const routes: Routes = [
  {path: "inventory-approval", component: InventryListComponent, canActivate: [AuthGuard]},
  {path: "inventory", component: InventoryComponent, canActivate: [AuthGuard]},
  {path: "", component: AccountComponent},
  {path: '**', redirectTo: ''}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
