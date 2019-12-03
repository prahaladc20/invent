import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Inventory} from "../inventory";

@Injectable({
  providedIn: 'root'
})
export class ApiService {


  API_URL = 'http://127.0.0.1:8000';
  httpHeaders = new HttpHeaders({'Content-Type': 'application/json'})

  constructor(private http: HttpClient) {
  }


  approvalProductes(): Observable<any> {
    return this.http.get(this.API_URL + '/getApprovalData/',
      {headers: this.httpHeaders});
  }

  masterProducts(): Observable<any> {
    return this.http.get(this.API_URL + '/getMasterData/',
      {headers: this.httpHeaders});
  }

  // It will hit master and assistant-approval both
  approveOrReject(inventory: Inventory): Observable<any> {
    console.log(inventory, "inventory Approve")
    var apiUrl = this.API_URL + '/inventory-approval/' + inventory['product_id'] + '/';
    if(inventory['action'] == 'create'){
      return this.http.post(this.API_URL + '/inventory-approval/approve/create/', inventory,
        {headers: this.httpHeaders});

    }else if (inventory['action'] == 'update') {
      return this.http.put(this.API_URL + '/inventory-approval/approve/update/' + inventory['product_id'] + '/', inventory,
        {headers: this.httpHeaders});

    } else if(inventory['action'] == 'delete'){
      return this.http.delete(this.API_URL + '/inventory-approval/approve/delete/' + inventory['product_id'] + '/',
        {headers: this.httpHeaders});
    }
    // alert(listing.product_name)
    
  }

// It will hit either master or assistant-approval depends on usertype
  createInventory(inventoty): Observable<any> {
    const listing = {
      author: 1,
      product_name: inventoty.product_name,
      vendor: inventoty.vendor,
      mrp: inventoty.mrp,
      batch_num: inventoty.batch_num,
      batch_date: inventoty.batch_date,
      quantity: inventoty.quantity,
      //   status: inventoty.status
    }
    // alert(listing.product_name)
    return this.http.post(this.API_URL + '/inventory/', listing,
      {headers: this.httpHeaders});
  }

// It will hit either master or assistant-approval depends on usertype
  updateInventory(inventory: Inventory): Observable<any> {
    // alert(listing.product_name)
    console.log(inventory, "UPDATE")

    return this.http.put(this.API_URL + '/inventory/update/' + inventory['product_id'] + '/', inventory,
      {headers: this.httpHeaders});

  }

// It will hit either master or assistant-approval depends on usertype

  deleteInventory(inventoryId): Observable<any> {
    // alert(listing.product_name)


  return this.http.delete(this.API_URL + '/inventory/delete/' + inventoryId + '/',
      {headers: this.httpHeaders});
  }

  // It will hit assistant-approval depends on usertype

  deleteApprovalInventory(inventoryId): Observable<any> {
    // alert(listing.product_name)


  return this.http.delete(this.API_URL + '/inventory-approval/delete/' + inventoryId + '/',
      {headers: this.httpHeaders});
  }

  // It will hit assistant-approval depends on usertype

  updateApprovalInventory(inventory: Inventory): Observable<any> {
    // alert(listing.product_name)


  return this.http.put(this.API_URL + '/inventory-approval/update/' + inventory['product_id'] + '/',inventory,
      {headers: this.httpHeaders});
  }


}
