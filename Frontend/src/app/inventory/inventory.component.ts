import {Component, OnInit} from '@angular/core';
import {Inventory} from "../inventory";
import {ApiService} from "../_service/api.service";
import {AccountService} from "../_service/account.service";
import {FormControl, FormGroup} from "@angular/forms";

@Component({
  selector: 'app-inventory',
  templateUrl: './inventory.component.html',
  styleUrls: ['./inventory.component.css']
})
export class InventoryComponent implements OnInit {
  selectedInventory: Inventory = null;
  inventories: Inventory[] = [
    {
      batch_date: '2019-11-24',
      status: 'Approved',
      batch_num: 1,
      mrp: 1,
      product_id: ' 1',
      product_name: 'string',
      quantity: 1,
      vendor: 'string',
    }


  ];
  userDisplayName = '';
  createForm: FormGroup;

  constructor(private api: ApiService, private accountService: AccountService) {
    this.createForm = new FormGroup({
      batch_date: new FormControl(''),
      batch_num: new FormControl(''),
      mrp: new FormControl(''),
      product_name: new FormControl(''),
      quantity: new FormControl(''),
      vendor: new FormControl(''),
      status: new FormControl('pending'),
      //   approved: new FormControl(false)
    });
    this.getProductes();
  }

  // userIsLogged() {
  // 	if(localStorage.getItem('token')) {
  // 		return true
  // 	} else {
  // 		return false
  // 	}
  // }

  getProductes = () => {
    this.api.masterProducts().subscribe(
      (data: Inventory[]) => {
        this.inventories = data;
        // console.log(data)
      },
      error => {
        console.log(error);
      }
    );
  }

  createInventory = () => {
    this.api.createInventory(this.createForm.value).subscribe(
      (data: Inventory) => {
        this.inventories.push(data)
        console.log(data);
      },
      error => {
        console.log(error)
      }
    );
  };

  deleteInventory = (inventoryId) => {
    const that = this;
    this.api.deleteInventory(inventoryId).subscribe(
      (data) => {
        this.inventories = this.inventories.filter((inventory) => {
          return inventory.product_id !== inventoryId;
        });
      },
      error => {
        console.log(error);
      }
    );
  };

  selectInventory = (inventoryId) => {
    this.selectedInventory = this.inventories.find((inventory) => {
      return inventory.product_id === inventoryId;
    });
  };


  ngOnInit() {
    this.userDisplayName = sessionStorage.getItem('loggedUser');
  }


  updateInventory() {
    this.api.updateInventory(this.selectedInventory).subscribe(
      (data) => {
      },
      error => {
        // this.selectedInventory = this.tempInventory;
      }
    );
  }


}
