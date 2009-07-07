/**
 * arguments: Tbl, field_list
 */

#include "cmysql.h"

class TestTableRow{
    public:
        TestTableRow(){init()};
        ~TestTableRow(){};
        int init();
        int iid;
        int iuin;
        string strname;
        string straddress;
}
typedef vector<TestTableRow> TestTableList;
class TestTableManager{
    public:
        TestTableManager();
        ~TestTableManager();
        int init_db(const char *sIp, const char *sUser, const char *sPsd, const char *sDbName);
        int close_db();
        int get_all(TestTableList &result_list);
        int get_all(const char *sSql, TestTableList &result_list);
        int get_one(const char *sSql, TestTableRow &result);
    private:
        int _load_field();
        CMysql _db;
}
void TestTableRow::init(){
    iid = 0;
    iuin = 0;
    strname = "";
    straddress = "";
}
int safe_atoi(const char*s){
    if(s==NULL)
        return 0;
    else
        return atoi(s);
}

TestTableManager::TestTableManager{
}
~TestTableManager::TestTableManager{
}

int TestTableManager::_load_field(TestTableRow &row){
    row.iid = safe_atoi(_db.GetField("id"));
    row.iuin = safe_atoi(_db.GetField("uin"));
    row.strname = _db.GetField("name");
    row.straddress = _db.GetField("address");
}
int TestTableManager::init_db(const char *sIp, const char *sUser, const char *sPsd, const char *sDbName){
    return _db.Init(sIp, sUser, sPsd, sDbName);
}
int TestTableManager::close_db(){
    _db.Close();
}
int TestTableManager::get_all(TestTableList &result_list){
    const char *sSql = "select * from TestTable;";
    return get_all(sSql, result_list);
}
int TestTableManager::get_all(const char *sSql, TestTableList &result_list){
    int iRet = _db.Query(sSql);
    if(iRet!=0){
        return iRet;
    }
    _db.StoreResult();
    TestTableRow row;
    while(_db.FetchRow()){
        row.init();
        _load_field(row);
        result_list.push_back(row);
    }
    _db.FreeResult();
}
int TestTableManager::get_one(const char *sSql, TestTableRow &result){
    int iRet = _db.Query(sSql);
    if(iRet!=0){
        return iRet;
    }
    _db.StoreResult();
    result.init();
    if(_db.FetchRow()){
        _load_field(result);
    }
    else{
        iRet = -1;
    }
    _db.FreeResult();
    return iRet;
}


