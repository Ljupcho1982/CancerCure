const B=require("../demo/pipeline.js"),assert=require("assert");
(async()=>{
 assert.strictEqual(B.parseAmount("1.450"),1450);assert.strictEqual(B.parseAmount("1.450,50"),1450.5);
 const cfg={maxAmount:10000,history:{EVN:1400},providers:{EVN:{domain:"evn.mk",account:"MK07300000000012345"},Vodovod:{domain:"vodovod.mk",account:"MK07200000000099887"}}};
 const em=[{id:"1",sender:"billing@evn.mk",subject:"Сметка за струја",body:"износ: 1.450 ден. Жиро-сметка: MK07300000000012345. Повикување на број: A1"},
  {id:"2",sender:"promo@shop.mk",subject:"попуст",body:"купи"},
  {id:"3",sender:"billing@vodovod.mk",subject:"Фактура",body:"Износ: 620 ден. Жиро-сметка: MK07200000000011111. Повикување на број: V1"}];
 const r=await B.run(em,cfg);
 assert.deepStrictEqual(r.map(x=>x.kind==="skipped"?"skip":x.status),["READY_FOR_APPROVAL","skip","BLOCKED"]);
 console.log("ok");
})();
