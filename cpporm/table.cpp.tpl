/**
 * arguments: Tbl, field_list
 */

#include "cmysql.h"

class ${Tbl}Row{
    public:
        ${Tbl}Row(){init()};
        ~${Tbl}Row(){};
        int init();
        % for field_name, field_type in field_list:
            % if field_type=='number':
        int i${field_name};
            % else:
        string str${field_name};
            % endif
        % endfor
}
typedef vector<${Tbl}Row> ${Tbl}List;
class ${Tbl}Manager{
    public:
        ${Tbl}Manager();
        ~${Tbl}Manager();
        int init_db(const char *sIp, const char *sUser, const char *sPsd, const char *sDbName);
        int close_db();
        int get_all(${Tbl}List &result_list);
        int get_all(const char *sSql, ${Tbl}List &result_list);
        int get_one(const char *sSql, ${Tbl}Row &result);
    private:
        int _load_field();
        CMysql _db;
}
void ${Tbl}Row::init(){
    % for field_name, field_type in field_list:
        % if field_type=='number':
    i${field_name} = 0;
        % else:
    str${field_name} = "";
        % endif
    % endfor
}
int safe_atoi(const char*s){
    if(s==NULL)
        return 0;
    else
        return atoi(s);
}

${Tbl}Manager::${Tbl}Manager{
}
~${Tbl}Manager::${Tbl}Manager{
}

int ${Tbl}Manager::_load_field(${Tbl}Row &row){
    % for field_name, field_type in field_list:
        % if field_type=='number':
    row.i${field_name} = safe_atoi(_db.GetField("${field_name}"));
        % else:
    row.str${field_name} = _db.GetField("${field_name}");
        % endif
    % endfor
}
int ${Tbl}Manager::init_db(const char *sIp, const char *sUser, const char *sPsd, const char *sDbName){
    return _db.Init(sIp, sUser, sPsd, sDbName);
}
int ${Tbl}Manager::close_db(){
    _db.Close();
}
int ${Tbl}Manager::get_all(${Tbl}List &result_list){
    const char *sSql = "select * from ${tbl};";
    return get_all(sSql, result_list);
}
int ${Tbl}Manager::get_all(const char *sSql, ${Tbl}List &result_list){
    int iRet = _db.Query(sSql);
    if(iRet!=0){
        return iRet;
    }
    _db.StoreResult();
    ${Tbl}Row row;
    while(_db.FetchRow()){
        row.init();
        _load_field(row);
        result_list.push_back(row);
    }
    _db.FreeResult();
}
int ${Tbl}Manager::get_one(const char *sSql, ${Tbl}Row &result){
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

