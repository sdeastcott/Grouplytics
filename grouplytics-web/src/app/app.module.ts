import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { SelectPageComponent } from './select-page/select-page.component';
import { ResultPageComponent } from './result-page/result-page.component';
import { GroupListSelectComponent } from './select-page/group-list-select/group-list-select.component';
import { GroupSelectComponent } from './select-page/group-list-select/group-select.component';
import { GroupListResultComponent } from './result-page/group-list-result.component';
import { GroupResultComponent } from './result-page/group-result.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SelectPageComponent,
    ResultPageComponent,
    GroupListSelectComponent,
    GroupSelectComponent,
    GroupListResultComponent,
    GroupResultComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
